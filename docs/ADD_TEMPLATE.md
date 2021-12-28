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
  "texts": [
    {
      "pos": [0, 0], // Initial position of text. First element of array is for the x axis and the second one is for the y axis.
      "size": [360, 120], // Max width and height the text can use
    }
  ]
}
```
