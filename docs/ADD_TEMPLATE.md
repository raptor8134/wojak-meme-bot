# Add template

## Structure

This project use the following structure for a template:

    .
    ├── config.json                   # Config of template
    └── template.jpg                  # Source file
    └── template.txt                  # Source file

The folder containing all this files will be used to access it.
MAKE SURE TO ADD YOUR TEMPLATE TO THE list.json FILE

## Config file

The JSON file needs to have the following structure

```js
{
    "name": "gigachad", // Template name (it must have the same name as the folder)
    "texts": [{
        "font_name": "Impact", // Font Family name (photo mode)
        "font_size": 50, // Font size (photo mode)
        "lw_multiplier": 2.5, // LW Multiplier (photo mode)
        "pos": [0, 0], // Initial position of text. First element of array is for the x axis and the second one is for the y axis. (photo mode)
        "img_width": 360, // Max width the text can use (photo mode)
        "ascii_width": 30 // Max width the text can use (ascii mode)
    }]
}
```
