<div align="center">
 <h1>Lindor candy detector in python</h1>
</div>

## Libraries needed
<ol>
<li>numpy</li>
<li>openCV</li>
</ol>

## How does it work? 🤔
the image is taken from a video of candies, then it's processed by using morphological methods and then creating bounding boxes in border of candies.
</br></br>
To check colors i use a range that was configured by testing on image earlier, then i check the dominant color and i check if it fits in range.
Then i set a bounding box with label of this candy and the color
</br></br>
To save positions and color of the candy i created a class, where i store all the information.

##
If someone has any sugestion what to modify or change let me know, but for now the project is finsihed.
