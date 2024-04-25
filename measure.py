import os


class LlamaChat:

    def __init__(self, model: str):
        self.model = model
        self.command = './main'

    def generate_response(self, input_text) -> str:
        """
        llama のモデルを使って、応答を生成する
        """
        base_prompt = ("# タスク \n"
                       "あなたは優秀なAIです. \n"
                       "ユーザーからの質問に対して即座に適切な回答を返してください. \n"
                       "質問は必ず簡潔に答えてください. \n"
                       "\n"
                       "User : こんにちは! \n"
                       "AI : こんにちは! 何かお手伝いできることはありますか? \n"
                       "User : 首の長い動物は何ですか? \n"
                       "AI : 首の長い動物はキリンです. \n"
                       f"User : {input_text}\n"
                       "AI : ").format(input_text)
        # llama.cpp を呼び出すためのコマンドを作成
        command = (
            f'{self.command} -m {self.model} -p "{base_prompt}" '
            f'-n 1024 --repeat-penalty 1.5  --temp 0.5 --top-p 0.3 --penalize-nl --top-k 10 '
            f'--color -e --log-disable --presence-penalty 1.2 --frequency-penalty 1.2')
        # コマンドを実行して、応答を取得
        response = os.popen(command).read()
        response = response.replace('0xef', '')
        response = response.replace('<s>', '')
        response = response.replace('</s>', '')

        # レスポンスの中でプロンプト以降の部分を抜き取る
        response = response.split('AI : ')[3]

        # 出力に空白行が複数連なっているところは1つだけに置き換える
        response = os.linesep.join([s for s in response.splitlines() if s])

        return response

    def chat(self, input_text: str):
        """
        ユーザーからの入力を受け取り、AI からの応答を返す
        """
        response = self.generate_response(input_text)

        return response


# 指定したディレクトリ以下にある .ggufファイルを一覧を取得
def get_gguf_files(directory) -> list:
    gguf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".gguf"):
                gguf_files.append(os.path.join(root, file))
    return gguf_files


def main():
    model_dir = "/Volumes/SSPA-USC/llama"
    models = get_gguf_files(model_dir)
    # ファイル名に ._ がついているものを除外する.
    models = [model for model in models if '._' not in model]
    for model in models:
        print(f'## {model}')
        chat = LlamaChat(model)

        message = 'もしAがBより速く走り、BがCより速く走るなら、AはCよりも速く走りますか？'

        # 例外が発生する場合は再度実行
        finished = False
        while not finished:
            try:
                response = chat.chat(message)
                print(f'Q : {message}')
                print(f'A : {response}')
                finished = True
            except:
                pass


if __name__ == '__main__':
    main()
