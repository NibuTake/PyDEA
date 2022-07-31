#

- 数理モデル説明
- ライブラリ活用例
- Communication
- References

## アーキテクチャ
- liner_model
    - LinerRegression
    - Ridge
        - () インスタンス化のみ。設定値を入れられる。
        - .fit
        - .coefなどで抽出

- attribute(instance variables)
    - rank of matrix X: fit後に追加されている
    - n_features: number of features
    -

- Method
    - fit
    - get_params
    - predict
    - score
    - set_params

## Architecture
- frontier_model
    - DEA
    - FDH
    - HierarchicalDEA

- DEA
    - init
        - formulation: str
            - multiple
            - envelope
        - orient: str
            - input
            - output
        - frontier: str
            - CRS
            - VRS

    - attributes
        - n_dmu
        - n_inputs
        - n_outputs

    - methods
        - get_results
        - fit
            - x: input np.array
            - y: output np.array
            - id: option np.array
