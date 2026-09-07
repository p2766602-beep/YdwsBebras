# YdwsBebras

國際運算思維挑戰賽（Bebras International Challenge on Informatics and Computational Thinking）歷屆題目數位化為繁體中文開放教材與題庫平台。

## 專案定位

本專案獨立開發，將 Bebras 國際各會員國公開釋出的年度題本（PDF）忠於原情境翻譯為繁體中文，做為開放式教學/自學教材使用。與台灣官方 Bebras 挑戰賽（教育部指導、國立臺灣師範大學資訊工程學系執行，`bebras.csie.ntnu.edu.tw`）無隸屬關係，亦不使用其任何未公開素材。

## 題目來源與授權

各國題本原文皆保留其官方授權聲明，翻譯／數位化後之衍生內容依 [CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/)（姓名標示－非商業性－相同方式分享）條款釋出，並標明原始出處。

| 來源 | 官方網站 | 已確認授權 |
|---|---|---|
| Bebras India | bebras.in | CC BY-NC-SA 4.0 |
| Informatik-Biber (Switzerland) | informatik-biber.ch | CC BY-NC-SA 4.0 |
| Lietuvos informatikos ir informatinio mąstymo konkursas (Lithuania) | — | CC BY-NC-SA 3.0 |
| Tekmovanje Bober (Slovenia) | tekmovanja.acm.si/bober | 題本內未標明CC授權，使用前需個別查證 |

## 資料夾結構

```
sources/<country>/          原始PDF＋擷取文字（不進版控，體積大，可隨時從官網重新取得）
data/                       題目結構化資料庫（task_uid／難度／年齡組／授權出處等）
assets/images/<country>/<year>/   題目圖片素材
translations/zh-TW/         翻譯後內容
platform/                   課程/題庫平台程式碼
```
