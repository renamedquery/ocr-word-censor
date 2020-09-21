import argparse, os, pytesseract, PIL, PIL.ImageEnhance, PIL.ImageDraw

# create an argument parser so that the user can pass command line arguments
parser = argparse.ArgumentParser(description = 'Censors the words on an image')
parser.add_argument('--input-file', '-i', type = str, help = 'Input file path', required = True)
parser.add_argument('--output-file', '-o', type = str, help = 'Output file path', required = True)
parser.add_argument('--word', '-w', type = str, help = 'Word to censor', required = True)
parser.add_argument('--color', '-c', type = str, help = 'Hex color to censor text with', required = True)

# parse the command line args
arguments = parser.parse_args()

# check that the input file exists, and if it doesnt then exit with an error
if (not os.path.exists(arguments.input_file)):
    print('Input file does not exist.')
    exit(1)


# open the image and increase its contrast
image = PIL.Image.open(arguments.input_file)
imageEnhancer = PIL.ImageEnhance.Sharpness(image)
image = imageEnhancer.enhance(2) # the optimal value seems to be 2; I have no idea why, but it works best this way

# create an object that can be used to draw on the image
imageDraw = PIL.ImageDraw.Draw(image)

'''
# convert the image to boxes that can be used to erase words
imageCharacterData = pytesseract.image_to_boxes(image, lang = 'eng')

# iterate through each character
for char in imageCharacterData.splitlines():
    charData = char.split(' ')
    coordinates = [
        int(charData[1]), # top left x coordinate
        image.size[1] - int(charData[2]), # top left y coordinate
        int(charData[3]), # bottom right x coordinate
        image.size[1] - int(charData[4]) # bottom right y coordinate
    ]
    text = charData[0]
    imageDraw.rectangle(coordinates, outline = '#00ff00')
'''

# convert the image to word data
imageData = pytesseract.image_to_data(image, lang = 'eng', output_type = pytesseract.Output.DICT)

# iterate through the words by their integer index and not their value
for index in range(len(imageData['text'])):
    if (imageData['text'][index].lower() == arguments.word.lower()):

        dimensions = [imageData['width'][index], imageData['height'][index]]
        position = [imageData['left'][index], imageData['top'][index]]

        print('MATCH FOUND AT X:{} Y:{}'.format(position[0], position[1]))

        imageDraw.rectangle([
            position[0],
            position[1],
            position[0] + dimensions[0],
            position[1] + dimensions[1]
        ], fill = arguments.color)

image.save(arguments.output_file)