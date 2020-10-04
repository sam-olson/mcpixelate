# mcpixelate

`mcpixelate` allows you to take any image and convert it into a Minecraft "mural". This is done by pixelating the image to a degree given by the user, and then converting each pixel to the nearest Minecraft block color (either concrete or terracotta).

For example, take this image of Dave Matthews:


First, it is necessary to create a PixelImage instance:
```python
from mcpixelate.mcpixelate import PixelImage

# create a pixelated version with a width of 140 pixels
# height is automatically calculated to maintain aspect ratio
dave = PixelImage("dave.jpg", 140, 0, 0)
```
To see what Dave looks like in a standard pixelated version:
```python
dave.pixelated_scaled.save("dave_natural.jpg")
```
And now, converted to Minecraft colors:
```python
dave.save_image("dave_minecraft.jpg")
```

It is also possible to print out the blocks needed to produce the mural...
```python
dave.display_blocks_needed()
```
...and to save which block is needed at each coordinate to a .csv file:
```python
dave.csv_coords("dave.csv")
```

