"use strict";
/**
 * @Time: 2025-03-03
 * @Auth: Adam Lyu
 */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var ai_text_analytics_1 = require("@azure/ai-text-analytics");
// Azure Text Analytics 配置
var TA_ENDPOINT = "https://demolyulanguageservice-v2.cognitiveservices.azure.com/";
var TA_KEY = "7wx94XIiJNNtz4cZIob3O10Q0GEIo46k3Oa3455PiWzEFEFgty28JQQJ99BBACBsN54XJ3w3AAAaACOG4WC8";
// 初始化客户端
var taClient = new ai_text_analytics_1.TextAnalyticsClient(TA_ENDPOINT, new ai_text_analytics_1.AzureKeyCredential(TA_KEY));
// 检测语言的函数
function detectLanguageWithAzure(text) {
    return __awaiter(this, void 0, void 0, function () {
        var response, result, successResult, detectedLang, error_1;
        var _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    _b.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, taClient.detectLanguage([text])];
                case 1:
                    response = _b.sent();
                    result = response[0];
                    if (result.error === undefined) {
                        successResult = result;
                        detectedLang = successResult.primaryLanguage.iso6391Name.toLowerCase();
                        return [2 /*return*/, {
                                language: detectedLang === 'fr' ? 'fr' : 'en',
                                confidence: (_a = successResult.primaryLanguage.confidenceScore) !== null && _a !== void 0 ? _a : 0
                            }];
                    }
                    else {
                        console.error("Language detection error:", result.error);
                        return [2 /*return*/, { language: 'en', confidence: 0 }];
                    }
                    return [3 /*break*/, 3];
                case 2:
                    error_1 = _b.sent();
                    console.error("Language detection failed:", error_1);
                    return [2 /*return*/, { language: 'en', confidence: 0 }];
                case 3: return [2 /*return*/];
            }
        });
    });
}
// 测试数据
var testCases = [
    { text: "Hello", expectedLanguage: "en" },
    { text: "Hi", expectedLanguage: "en" },
    { text: "Bonjour", expectedLanguage: "fr" },
    { text: "Salut", expectedLanguage: "fr" },
    { text: "Good morning", expectedLanguage: "en" },
    { text: "Bon matin", expectedLanguage: "fr" },
    { text: "How are you", expectedLanguage: "en" },
    { text: "Comment vas-tu", expectedLanguage: "fr" },
    { text: "What’s up", expectedLanguage: "en" },
    { text: "Quoi de neuf", expectedLanguage: "fr" },
    { text: "I’d like to ask a question", expectedLanguage: "en" },
    { text: "J’aimerais poser une question", expectedLanguage: "fr" },
    { text: "I am not feeling well", expectedLanguage: "en" },
    { text: "Je ne me sens pas bien", expectedLanguage: "fr" },
    { text: "What is the Personalized Health Education Program", expectedLanguage: "en" },
    { text: "How can I navigate the Canadian health care system", expectedLanguage: "en" },
    { text: "Où puis-je trouver des ressources de bien-être", expectedLanguage: "fr" },
    { text: "I have a cough that won't go away", expectedLanguage: "en" },
    { text: "J’ai une toux qui ne disparaît pas", expectedLanguage: "fr" },
    { text: "My throat is bothering me", expectedLanguage: "en" },
    { text: "Ma gorge me dérange", expectedLanguage: "fr" },
    { text: "I need a renewal for my prescription", expectedLanguage: "en" },
    { text: "J’ai besoin de renouveler mon ordonnance", expectedLanguage: "fr" },
    { text: "I jammed my finger while playing basketball", expectedLanguage: "en" },
    { text: "Je me suis coincé le doigt en jouant au basket", expectedLanguage: "fr" },
    { text: "My elbow hurts when I bend it", expectedLanguage: "en" },
    { text: "Mon coude me fait mal quand je le plie", expectedLanguage: "fr" },
    { text: "I have shortness of breath when I exercise", expectedLanguage: "en" },
    { text: "J’ai du mal à respirer quand je fais de l’exercice", expectedLanguage: "fr" },
    { text: "Je n’ai plus de questions, merci", expectedLanguage: "fr" },
    { text: "That’s all I needed, bye", expectedLanguage: "en" },
    { text: "C’est tout ce dont j’avais besoin, au revoir", expectedLanguage: "fr" },
    { text: "I think I’m all set, have a great day", expectedLanguage: "en" },
    { text: "Je crois que c’est tout, bonne journée", expectedLanguage: "fr" },
    { text: "I have a sore throat", expectedLanguage: "en" },
    { text: "J’ai mal à la gorge", expectedLanguage: "fr" },
    { text: "I need to get tested for TB", expectedLanguage: "en" },
    { text: "J’ai besoin de me faire tester pour la tuberculose", expectedLanguage: "fr" },
    { text: "I would like to start using some kind of contraception", expectedLanguage: "en" },
    { text: "Je voudrais commencer à utiliser une contraception", expectedLanguage: "fr" },
    { text: "I have pain urinating", expectedLanguage: "en" },
    { text: "J’ai mal en urinant", expectedLanguage: "fr" },
    { text: "I would like to take a pregnancy test", expectedLanguage: "en" },
    { text: "Je voudrais faire un test de grossesse", expectedLanguage: "fr" },
    { text: "I don’t have any more questions, thanks", expectedLanguage: "en" },
    { text: "Merci, je n’ai plus de questions", expectedLanguage: "fr" },
    { text: "I’m good for now. Talk later", expectedLanguage: "en" },
    { text: "Tout est bon pour moi. À bientôt", expectedLanguage: "fr" },
    { text: "I have swelling on my face after an injury", expectedLanguage: "en" },
    { text: "J’ai un gonflement au visage après une blessure", expectedLanguage: "fr" },
];
// 测试函数
function runTests() {
    return __awaiter(this, void 0, void 0, function () {
        var correct, total, _i, testCases_1, testCase, result, isCorrect, accuracy;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    correct = 0;
                    total = testCases.length;
                    _i = 0, testCases_1 = testCases;
                    _a.label = 1;
                case 1:
                    if (!(_i < testCases_1.length)) return [3 /*break*/, 4];
                    testCase = testCases_1[_i];
                    return [4 /*yield*/, detectLanguageWithAzure(testCase.text)];
                case 2:
                    result = _a.sent();
                    isCorrect = result.language === testCase.expectedLanguage;
                    if (isCorrect)
                        correct++;
                    console.log("Text: \"".concat(testCase.text, "\""));
                    console.log("Expected: ".concat(testCase.expectedLanguage, ", Detected: ").concat(result.language, ", Confidence: ").concat(result.confidence));
                    console.log("Result: ".concat(isCorrect ? "Correct" : "Incorrect"));
                    console.log("---");
                    _a.label = 3;
                case 3:
                    _i++;
                    return [3 /*break*/, 1];
                case 4:
                    accuracy = (correct / total) * 100;
                    console.log("Total Tests: ".concat(total));
                    console.log("Correct: ".concat(correct));
                    console.log("Accuracy: ".concat(accuracy.toFixed(2), "%"));
                    return [2 /*return*/];
            }
        });
    });
}
// 执行测试
if (require.main === module) {
    runTests().catch(function (err) { return console.error("Test execution failed:", err); });
}
