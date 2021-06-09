# crack
ひび割れのシミュレーション

概要
ゴムで繋がった正方格子があって、そのゴムがだんだん弱くなってきてある限界の長さになると切れます。切れたところの節は移動してさらに切れやすくなってどんどん裂け目が広がっていくというシミュレーションです。
パラメータを変えるとこんな絵というか動画GIFが出力されます。
![20210606172044_out](https://user-images.githubusercontent.com/43979686/121297184-e30dab80-c92c-11eb-890e-9cea25678d10.gif)
![20210605183046_out](https://user-images.githubusercontent.com/43979686/121297212-f28cf480-c92c-11eb-8157-cf3c4750e96d.gif)
使い方
起動してstartボタンを押します。startボタンを押すまでは何も起こりません。
startボタンを押すと、まともなパラメータが設定されている場合は何かが起こります。ゴムが切れてひび割れが広がっていく様子が見れます。
stopボタンを押すと、画面の更新が泊まります。放置しているとメモリがどんどん食われていって最大１０００コマ分のメモリが消費されてしまいます。
write GIFボタンを押すと、GIFアニメーションファイルを出力します。同時にパラメータファイルも出力します。パラメータファイルは同じ設定を再現したいときに使います。
制限
ボタンを押す順番を間違えると何が起こるかわかりません。たとえばstopのあとstartを押すとか。
現状ではパラメータを設定するダイアログのようなものはありません。ソースファイルを直接いじって効果を試しています。
