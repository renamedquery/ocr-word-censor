import argparse, os, pytesseract, PIL, PIL.ImageEnhance, PIL.ImageDraw, string

# create an argument parser so that the user can pass command line arguments
parser = argparse.ArgumentParser(description = 'Censors the words on an image')
parser.add_argument('--input-file', '-i', type = str, help = 'Input file path', required = True)
parser.add_argument('--output-file', '-o', type = str, help = 'Output file path', required = True)
parser.add_argument('--word', '-w', type = str, help = 'Word to censor', required = True)
parser.add_argument('--color', '-c', type = str, help = 'Hex color to censor text with', required = True)
parser.add_argument('--debug-mode', '-d', action = 'store_true')

# parse the command line args
arguments = parser.parse_args()

# check that the input file exists, and if it doesnt then exit with an error
if (not os.path.exists(arguments.input_file)):
    print('Input file does not exist.')
    exit(1)

# open the image and increase its contrast
image = PIL.Image.open(arguments.input_file)
imageEnhancer = PIL.ImageEnhance.Sharpness(image.convert('RGBA'))
image = imageEnhancer.enhance(2) # the optimal value seems to be 2; I have no idea why, but it works best this way

# create an object that can be used to draw on the image
imageDraw = PIL.ImageDraw.Draw(image)

# convert the image to word data (using a black and white version "LA")
imageData = pytesseract.image_to_data(image.convert('LA').convert('RGBA'), lang = 'eng', output_type = pytesseract.Output.DICT)

# iterate through the words by their integer index and not their value
for index in range(len(imageData['text'])):

    dimensions = [imageData['width'][index], imageData['height'][index]]
    position = [imageData['left'][index], imageData['top'][index]]

    # get the word and touch it up by replacing 0s with Os and removing periods, commas, and exclamation marks
    currentWord = imageData['text'][index].lower()
    currentWord = currentWord.replace('0', 'o')

    isMatch = currentWord.lower() == arguments.word.lower() or arguments.word.lower() in currentWord.lower()

    if isMatch: print('MATCH FOUND AT X:{} Y:{}'.format(position[0], position[1]))

    # if the program isnt running under debug mode then censor the words as normal (make everything lowercase since the program is case insensitive)
    if (isMatch and not arguments.debug_mode):

        imageDraw.rectangle([
            position[0],
            position[1],
            position[0] + dimensions[0],
            position[1] + dimensions[1]
        ], fill = arguments.color)
    
    elif (arguments.debug_mode):

        imageDraw.rectangle([
            position[0],
            position[1],
            position[0] + dimensions[0],
            position[1] + dimensions[1]
        ], outline = '#00ff00' if isMatch else '#ff0000')

image.save(arguments.output_file)