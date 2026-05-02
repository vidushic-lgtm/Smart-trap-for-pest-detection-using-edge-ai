import sensor, image, time, ml, math, uos, gc

# -------------------- Camera Setup --------------------
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240))
sensor.skip_frames(time=2000)

# -------------------- Load Model --------------------
try:
    net = ml.Model("trained.tflite", load_to_fb=True)
except Exception as e:
    raise Exception('Model load failed: ' + str(e))

# -------------------- Load Labels --------------------
try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Labels load failed: ' + str(e))

# -------------------- Settings --------------------
min_confidence = 0.4

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
]

threshold_list = [(math.ceil(min_confidence * 255), 255)]

# -------------------- FOMO Post Processing --------------------
def fomo_post_process(model, inputs, outputs):
    ob, oh, ow, oc = model.output_shape[0]

    x_scale = inputs[0].roi[2] / ow
    y_scale = inputs[0].roi[3] / oh
    scale = min(x_scale, y_scale)

    x_offset = ((inputs[0].roi[2] - (ow * scale)) / 2) + inputs[0].roi[0]
    y_offset = ((inputs[0].roi[3] - (oh * scale)) / 2) + inputs[0].roi[1]

    detections = [[] for _ in range(oc)]

    # ✅ FIX: extract scalar values from tuple
    scale_q = model.output_scale[0]
    zero_point = model.output_zero_point[0]

    for i in range(oc):

        out = outputs[0][0, :, :, i]

        h = out.shape[0]
        w = out.shape[1]

        # Create grayscale image
        img = image.Image(w, h, image.GRAYSCALE)

        # Convert int8 → usable pixel values
        for y in range(h):
            for x in range(w):
                val = (out[y][x] - zero_point) * scale_q   # int8 → float
                val = int(max(0, min(255, val * 255)))     # scale to 0–255
                img.set_pixel(x, y, val)

        blobs = img.find_blobs(
            threshold_list,
            x_stride=1,
            y_stride=1,
            area_threshold=1,
            pixels_threshold=1
        )

        for b in blobs:
            x, y, w, h = b.rect()

            score = img.get_statistics(
                thresholds=threshold_list,
                roi=b.rect()
            ).l_mean() / 255.0

            x = int((x * scale) + x_offset)
            y = int((y * scale) + y_offset)
            w = int(w * scale)
            h = int(h * scale)

            detections[i].append((x, y, w, h, score))

    return detections

# -------------------- Main Loop --------------------
clock = time.clock()

while True:
    clock.tick()

    img = sensor.snapshot()

    for i, detection_list in enumerate(net.predict([img], callback=fomo_post_process)):

        if i == 0:
            continue  # background

        if not detection_list:
            continue

        print("********** %s **********" % labels[i])

        for x, y, w, h, score in detection_list:
            cx = int(x + w / 2)
            cy = int(y + h / 2)

            print("x:", cx, "y:", cy, "score:", score)

            img.draw_circle((cx, cy, 12), color=colors[i])

    print("FPS:", clock.fps(), "\n")
