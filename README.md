# STEP_GOOGLE_HW3
pythonCalculation.py は宿題(1)のコードです。
pythonCalculation2.pyは宿題(2)のコードです。
詳しい説明はpythonCalculation.pyの中にあります。
pythonCalculation2.pyにはpythonCalculation.pyと違うところを説明しております。

#追加
c++で宿題(2)を実現しました。考えは前のと同じですが、C++では、関数に変数の参照渡しができますので、メモリの消費を抑えられます。例えば、pythonではかっこ内の部分をコピーして再帰で計算を行いますが、C++だとtokensの参照とかっこの場所を示すindexの参照を関数に渡せればいいです。tokensのかっこの部分のコピーを取る必要がなくなります。