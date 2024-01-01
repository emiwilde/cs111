import sys
from byuimage import Image


def validate_commands(lst, ):
   if lst[1] == "-d" and len(lst) > 2:
      return True
   elif lst[1] == "-k" and len(lst) >= 5:
      filename = lst[2]
      percent = lst[4]
      output_file = lst[3]
      darkened_image = darken(filename, percent)
      darkened_image.save(output_file)
      return True
   elif lst[1] == "-s" and len(lst) >= 4:
      filename = lst[2]
      output_file = lst[3]
      sepia_image = sepia(filename)
      sepia_image.save(output_file)
   elif lst[1] == "-g":
      filename = lst[2]
      grayed_image = grayscale(filename)
      output_file = lst[3]
      grayed_image.save(output_file)
      return True
   elif lst[1] == "-b" and len(lst) >= 8:
      filename = lst[2]
      output_file = lst[3]
      thickness = lst[4]
      red = lst[5]
      green = lst[6]
      blue = lst[7]
      bordered_image = make_borders(filename, thickness, red, green, blue)
      bordered_image.save(output_file)
   elif lst[1] == "-f" and len(lst) >= 4:
      filename = lst[2]
      output_file = lst[3]
      flipped_image = flipped(filename)
      flipped_image.save(output_file)
   elif lst[1] == "-m" and len(lst) >= 4:
      filename = lst[2]
      output_file = lst[3]
      mirrored_image = mirror(filename)
      mirrored_image.save(output_file)
   elif lst[1] == "-c" and len(lst) >= 8:
      image1 = lst[2]
      image2 = lst[3]
      image3 = lst[4]
      image4 = lst[5]
      output_file = lst[6]
      thickness = lst[7]
      collage_result = collage(image1, image2, image3, image4, thickness)
      collage_result.save(output_file)
   elif lst[1] == "-y" and len(lst) >= 7:
      forground_image = lst[2]
      background_image = lst[3]
      output_file = lst[4]
      threshold = lst[5]
      factor = lst[6]
      greenscreen_result = green_screen(forground_image, background_image)
      greenscreen_result.save(output_file)
   else:
      return False


def sepia(filename):
      image = Image(filename)
      for y in range(image.height):
         for x in range(image.width):
            pixel = image.get_pixel(x, y)
            true_red = 0.393 * pixel.red + 0.769 * pixel.green + 0.189 * pixel.blue
            true_green = 0.349 * pixel.red + 0.686 * pixel.green + 0.168 * pixel.blue
            true_blue = 0.272 * pixel.red + 0.534 * pixel.green + 0.131 * pixel.blue
            if pixel.red > 255:
               pixel.red = 255
            pixel.red = true_red
            if pixel.green > 255:
               pixel.green = 255
            pixel.green = true_green
            if pixel.blue > 255:
               pixel.blue = 255
            pixel.blue = true_blue
      return image
def darken(filename, percent):
   image = Image(filename)
   percent = float(percent)
   darkened_percent = 1.0 - percent
   for pixel in image:
      pixel.red = pixel.red * darkened_percent
      pixel.green = pixel.green * darkened_percent
      pixel.blue = pixel.blue * darkened_percent
   return image


def grayscale(filename):
   image = Image(filename)
   for y in range(image.height):
      for x in range(image.width):
         pixel = image.get_pixel(x, y)
         average = (pixel.red + pixel.green + pixel.blue) / 3
         pixel.red = average
         pixel.green = average
         pixel.blue = average
   return image


def make_borders(filename, thickness, rvalue, gvalue, bvalue):
   image = Image(filename)
   thickness1 = int(thickness)
   red = int(rvalue)
   green = int(gvalue)
   blue = int(bvalue)
   new_width = image.width + 2 * thickness1
   new_height = image.height + 2 * thickness1
   new_image = Image.blank(new_width, new_height)
   for y in range(new_height):
      for x in range(new_width):
         if x < thickness1 or x >= thickness1 + image.width or y < thickness1 or y >= thickness1 + image.height:
            pixel_new = new_image.get_pixel(x, y)
            pixel_new.red = red
            pixel_new.green = green
            pixel_new.blue = blue#
         else:
            original_x = x - thickness1
            original_y = y - thickness1
            if original_x >= 0 and original_y >= 0:
               pixel = image.get_pixel(original_x, original_y)
               pixel_new = new_image.get_pixel(x, y)
               pixel_new.red = pixel.red
               pixel_new.green = pixel.green
               pixel_new.blue = pixel.blue
   return new_image

def flipped(filename):
   image = Image(filename)
   new_image = Image.blank(image.width, image.height)
   for y in range(image.height):
      for x in range(image.width):
         pixel = image.get_pixel(x, y)
         pixel_new = new_image.get_pixel(x, image.height - y - 1)
         pixel_new.red = pixel.red
         pixel_new.green = pixel.green
         pixel_new.blue = pixel.blue
   return new_image

def mirror(filename):
   image = Image(filename)
   new_image = Image.blank(image.width, image.height)
   for y in range(image.height):
      for x in range(image.width):
         pixel = image.get_pixel(x, y)
         pixel_new = new_image.get_pixel(image.width - x - 1, y)
         pixel_new.red = pixel.red
         pixel_new.green = pixel.green
         pixel_new.blue = pixel.blue
   return new_image


def collage(image1, image2, image3, image4, thickness):
   image1 = Image(image1)
   image2 = Image(image2)
   image3 = Image(image3)
   image4 = Image(image4)
   thickness1 = int(thickness)
   new_width = (image1.width * 2) + (thickness1 * 2) + 10#((image1.width + 2 * thickness1) * 2)
   new_height = (image1.height * 2) + (thickness1 * 2) + 10#((image1.height + 2 * thickness1) * 2)
   background = Image.blank(new_width, new_height)
   x1 = thickness1
   x2 = thickness1 + image1.width
   y1 = thickness1
   y2 = thickness1 + image1.height
   for y in range(new_height):
      for x in range(new_width):
         pixel_new = background.get_pixel(x, y)
         pixel_new.red = 0
         pixel_new.green = 0
         pixel_new.blue = 0
   for y in range(new_height):
      for x in range(new_width):
         if (x < x1 and y < y1) or (x >= x2 and y < y1):
            pixel = image1.get_pixel(x- x1, y - y1)
         elif (x > x1 and y < y1) or (x >= x2 and y >= y2):
            pixel = image2.get_pixel(x - x2, y - y1)
         elif (x < x1 and y >= y2) or (x >= x2 and y >= y2):
            pixel = image3.get_pixel(x - x1, y - y2)
         else:
            pixel = image4.get_pixel(x, y)

   return background



def detect_green(pixel):
   factor = 1.3
   threshold = 90
   average = (pixel.red + pixel.green + pixel.blue) / 3
   if pixel.green >= factor * average and pixel.green > threshold:
      return True
   else:
      return False


def green_screen(foreground, background):
   foreground = Image(foreground)
   background = Image(background)
   final = Image.blank(background.width, background.height)
   for y in range(background.height):
      for x in range(background.width):
         fp = final.get_pixel(x, y)
         bp = background.get_pixel(x, y)
         fp.red = bp.red
         fp.green = bp.green
         fp.blue = bp.blue
   for y in range(foreground.height):
      for x in range(foreground.width):
         fp = foreground.get_pixel(x, y)
         if not detect_green(fp):
            np = final.get_pixel(x, y)
            np.red = fp.red
            np.green = fp.green
            np.blue = fp.blue
   return final


def return_image(filename):
   beach_image = Image(filename)
   beach_image.show()


if __name__ == "__main__":
   list_args = sys.argv[0:]

   if validate_commands(list_args):
      image_filename = list_args[2]
      return_image(image_filename)
   else:
      print("not found")
