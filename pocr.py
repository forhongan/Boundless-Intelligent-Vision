import config_reader
input_path=config_reader.config['path']['orc_input_path']

from paddlex import create_pipeline

pipeline = create_pipeline(pipeline="OCR")
output = pipeline.predict([input_path])
for res in output:
    res.print()
    res.save_to_img("./output/")
    res.save_to_json("./output/")