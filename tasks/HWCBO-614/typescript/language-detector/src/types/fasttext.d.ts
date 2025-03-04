declare module 'fasttext.js' {
  class FastText {
    constructor(options: { loadModel: string });
    load(): Promise<void>;
    predict(text: string, k?: number): Promise<{ label: string; value: number }[]>;
  }
  export default FastText;
}