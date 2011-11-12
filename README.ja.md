# Build script for Android project.



## 使いかた
Androidプロジェクト直下にファイルを置き、実行します

    $ build.py
.apkファイルが "\<project.name\>_\<versionName\>.\<versionCode\>.apk" に作られます。

もしプロジェクトディレクトリ下に "build.xml" ファイルが無い場合、先に下記コマンドを実行してください。
    $ android update project -p .



## スクリプトの処理内容
以下の処理を行ないます

1. ビルド前に"AndroidManifest.xml"を更新します

    1.1 android:debuggableを "false" に置換

    1.2 android:versionCodeをインクリメント

1. "res/values/copyright.xml"を生成もしくは更新します

1. Antによるビルドを実行します（$ ant release）

1. .apkファイルのファイル名を変更します

1. 再び"AndroidManifest.xml"を更新します

    5.1 android:debuggableを "true" に置換



## 注意事項：スクリプトが自動生成するファイルについて

1. build.version

    ビルド時にインクリメントした "android:versionCode" が格納され、次のビルドで使用されます。
    ".gitignore"ファイルに追加しておくことをおすすめします。

1. res/values/copyright.xml

    アプリ内でCopyright表示に使うための"年"が書きこまれます。
    都度上書きされますので、他の\<string\>を追加するなどしても消えてしまいます。

    ただし、"copyright_year_to"の値が未来年の場合、値は上書きされません
    （今年に戻されることはありません）。

