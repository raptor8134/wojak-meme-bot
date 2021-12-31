# Add template

## Structure

This project use the following structure for a template:

    .
    ├── config.json                   # Config of template
    └── template.jpg                  # Source file

The folder containing all this files will be used to access it.
MAKE SURE TO ADD YOUR TEMPLATE TO THE list.json FILE

## Config file

The JSON file needs to have the following structure

```js
{
    "texts": [{
        "font_name": "Impact", // Font Family name
        "font_size": 50,
        "lw_multiplier": 2.5,
        "pos": [0, 0], // Initial position of text. First element of array is for the x axis and the second one is for the y axis.
        "width": 360, // Max width the text can use
    }]
}
```
