# Build script for Android project.
Androidプロジェクト用のビルドスクリプトです。



# 使いかた
Androidプロジェクト直下にpuild.pyファイルを置き、実行します。

    $ build.py

完了すると、.apkファイルが bin/\<project.name\>_\<versionName\>.\<versionCode\>.apk に出力されます。

もしプロジェクトディレクトリ下にbuild.xmlファイルが無い場合、先に下記コマンドを実行してください。

    $ android update project -p .



# スクリプトの処理内容
本スクリプトは、以下の処理を行ないます。

1. ビルド前にAndroidManifest.xmlを更新します

    1.1 android:debuggableをfalseに置換

    1.2 android:versionCodeをインクリメント

1. res/values/copyright.xmlを生成もしくは更新します

1. Antによるビルドを実行します（$ ant release）

1. .apkファイルのファイル名を変更します（フォーマットは上記）

1. 再びAndroidManifest.xmlを更新します

    5.1 android:debuggableをtrueに置換



# 注意事項：スクリプトが自動生成するファイルについて

### build.version

ビルド時にインクリメントしたandroid:versionCodeが格納され、次のビルドで使用されます。

ブランチを切り替えても常にandroid:versionCodeが前に進むようにするために
VCSのignoreファイルに追加しておくことをおすすめします。


### res/values/copyright.xml

アプリ内でCopyright表示に使うための"年"が書きこまれます。
ビルドの都度上書きされますので、他の\<string\>を追加するなどしても消えてしまいます。

ただし、"copyright\_year\_to"の値が未来年の場合、値は上書きされません
（今年に戻されてしまうことはありません）。
