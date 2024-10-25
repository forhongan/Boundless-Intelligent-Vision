from paddlex import create_pipeline

pipeline = create_pipeline(pipeline="OCR")
output = pipeline.predict(['images_test/test1.png'])
for res in output:
    res.print()
    res.save_to_img("./output/")
    res.save_to_json("./output/")