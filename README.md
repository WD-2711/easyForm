# EasyForm

![](../../source/images/README/easyform-v1-red.svg)

------



## Introduction

​	This demo is to fill **JinShan** online survey. First, it use **tencent OCR tools** to extract infomation from many pictures. Second, it submit data to online survey using **selenium**.

## Environment

| name        | version     |
| ----------- | ----------- |
| python      | 3.6         |
| firefox     | 108.0.1 x64 |
| geckodriver | lastest     |

## Form Format

​	It's for JinShan online survey, the picture corresponding to this form is as follows.

![](../../source/images/README/1.png)

## Usage

1. Configure `config.yaml`.

| name                          | description                             |
| ----------------------------- | --------------------------------------- |
| SecretId & SecretKey          | Tencent OCR key                         |
| FormUrl                       | The online survey                       |
| FirefoxPath & GeckoDriverPath | Selenium setting                        |
| UserName & PassWd             | JinShan Account                         |
| FormImagePath                 | The image you want submit               |
| TableImagePath                | Information extracted from these images |
| ExcelPath                     | Middle files when extracting infomation |
| InfoPath                      | Information extract result              |
| Number                        | How many surveys you want to submit     |

2. Enter the following command.

```python
python3 infoExtracter.py && python3 formSubmiter.py
```