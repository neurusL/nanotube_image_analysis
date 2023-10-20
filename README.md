# Nanotube Image Analysis

Description of project to be filled...

## Environment 
The program is developed under:
`Python`      3.9.13    \
And following modules are used: \
`scikit-image`     0.19.2  (requires Python >= 3.6)  \
`matplotlib`  3.5.2         \
`cv2`         4.7.0.72         \
`NumPy`       1.21.5        

If any of above module is not installed, use the package manager [pip](https://pip.pypa.io/en/stable/) to install 
```bash
pip3 install <module>
```
Or install all above using
```bash
pip3 install -r requirements.txt

```
## Usage 
```bash
main.py [-h] -f functionality [-m mode] [-l image load path] [-s image save path]
```

Functionality:
Currently we only support following nanotube image analysis: itd (estimating average intertube distance), circle (find the largest circle fit between nanotubes)

ITD: Calculate average intertube distance of nanotubes in the image, there are three 
modes of usage:
- ```-m example``` will simply show you examples of how this program process image and results of calculated itds
- ```-m without-origin``` will process any input SEM image of nanotubes and give
processed image and calculated itds
- ```-m over-origin``` will process any input SEM image of nanotubes and give
processed image **stacked over original image** and calculated itds


 | arguments | descriptions |
 | :--- | :--- |
 | ```-h, --help```            | show this help message and exit |
| ```-f functionality, --func functionality```  | functionality can be: itd, circle |
 | ```-m mode, --mode mode```  | mode can be: example, without-origin, or over-origin |
 | ```-l image load path, --loadpath image load path``` | path of image to be loaded |
 | ```-s image save path, --savepath image save path``` | path to save image, default is in ```/result``` |

## Examples
```bash
python3 main.py -f 'itd' -m example
```
```bash
python3 main.py -f 'itd' --mode without-origin --loadpath 'data/CNT Sample 1.tif' --savepath 'results/Sample1_result.jpg'
```
```bash
python3 main.py -f 'itd' --mode over-origin --loadpath 'data/CNT Sample 1.tif' --savepath 'results/Sample1_result_overorigin.jpg'
```

```bash
python3 main.py -f 'circle'  --loadpath 'data/CNT Sample 1.tif' --savepath 'results/Sample1_result_largest_circle.jpg'
```

