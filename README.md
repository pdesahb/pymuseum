# PyMuseum

A simple Python tool to scrap and create beautiful wallpapers.

## Installation

To install, execute this in your shell:

```bash
git clone https://github.com/pdesahb/pymuseum.git
cd pymuseum
pip install -r requirements.txt
python setup.py install
```

## Usage

You can use PyMuseum in two modes:
* scrapping will download images from the web and transform them. Currently supported sources are:
    * [reddit](https://reddit.com): with beautiful subreddits such as [/r/museum](https://reddit.com/r/museum) or [/r/lepetitmusee](https://reddit.com/r/lepetitmusee)
    * [artuk](https://artuk.org/) who offers a large collection of paintings from the UK
    * more sources are comming, contributions are welcome!

* transformation will simply transform your local images

For instance to get the top 50 images of all time from [/r/museum](https://reddit.com/r/museum) on your Desktop:
```bash
pymuseum scrap -to ~/Desktop -n 50 reddit museum -top all
```

To see all other usage:

```bash
pymuseum --help
```

Example of result

![Mona Lisa transformed through PyMuseum](https://raw.githubusercontent.com/pdesahb/pymuseum/master/assets/monalisa.jpg)
[Original image from Wikipedia](https://fr.wikipedia.org/wiki/La_Joconde#/media/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg)

## Authors

* **Pierre de Sahb** - *Initial work* - [pdesahb](https://github.com/pdesahb)

See also the list of [contributors](https://github.com/pdesahb/pymuseum/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* This project was totally inspired by [this blog post](http://archagon.net/blog/2018/05/02/a-native-art-gallery-for-your-mac/)
