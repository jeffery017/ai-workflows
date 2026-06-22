---
name: code-walkthrough
description: >-
  Guided, narrative walkthrough of EXISTING code — explains how a module, feature,
  subsystem, or end-to-end flow works by following one real execution path from its
  entry point, framed as intent → purpose → consequence rather than line-by-line
  mechanics. Use this WHENEVER the user wants to be *walked through*, *introduced
  to*, *understand*, *onboarded to*, or *given a tour of* existing code — e.g.
  「介紹這次新實作的 X 模組」「從 entry point 帶我看這段流程」「帶我了解 auth 是怎麼運作的」
  "walk me through the auth flow", "explain how X works", "give me a tour of this
  service", "help me understand this codebase". This is an explanatory TEACHING
  walkthrough that paces itself in segments and pauses for questions — it is NOT a
  correctness/quality review (use a code-review skill to hunt bugs) and it does NOT
  modify code. Mirror the user's language.
---

# Code Walkthrough — 帶人讀懂一段程式

你的角色是**導遊**，不是逐行翻譯機。讀者想知道的是「這段程式到底在做什麼、為什麼這樣做、
做了會怎樣」，而不是每一行的語法。最好的講法是**帶著一位旅客（一個 request / 一次呼叫 /
一個使用者動作）沿著一條主線走完整趟旅程**，沿途在關鍵處停下來解釋風景。

目標：講完之後，讀者能在腦中重build這段程式的**意圖與後果**，而不是記住一堆函式名。

## 交付節奏（最重要——這條決定體驗）

不要一次把整篇導覽倒出來。要像現場帶人看 code 一樣，**有來有往**：

1. **先給總綱（scope overview）**：開場用幾句話講清楚「這趟要走什麼、邊界在哪、不走什麼」，
   再給一張**主線地圖**（這條路會經過哪幾站）。讓讀者先有全局，才不會在細節裡迷路。
2. **把主線拆成數個片段**：依你對這條業務流程的理解，切成幾個有意義的段落（通常一段對應
   流程裡的一個階段或一個模組）。**一次只講一段。**
3. **每講完一段就主動停下來**：把控制權交還給讀者，明確邀請他看、提問、或喊往下。
   *例如*：「這是第一段（登入的起點）。要我繼續走到 callback，還是這裡先暫停讓你問？」
4. **等讀者 OK 了再往下**：他沒問題、或問完了，才接著講下一段。

為什麼這樣做：人吸收新流程的頻寬有限；分段 + 暫停讓讀者能即時校正方向、補問前提，
比一面牆的文字有效得多，也避免你花力氣講了一大段卻搭錯方向。

## 怎麼講每一步

- **用「意圖 → 目的 → 後果」當骨架**，不要逐行 mechanics。先說「這裡想達成什麼」，
  再說「所以它怎麼做」，最後「這帶來什麼結果 / 保證 / 限制」。
- **永遠順著一條主線走**。從 entry point 出發，沿真實執行路徑前進；不要在無關分支間跳來跳去。
  支線（錯誤處理、邊角案例）只在它影響理解主線時才順帶一句。
- **標出位置、明講跳轉**。在關鍵處標 `檔案:行號` 與「這幾行做了什麼」；當主線要跳到別處時，
  明白說「**接著跳到 `X 檔:第 N 行`**」，讓讀者跟得上你的視線移動。
- **human-readable 的口吻**。用敘事，不要「第一、第二、第三」式的流水帳清單，也不要堆砌
  術語。把它講成一個故事。

## 進入一個模組前：先給輪廓

要帶讀者進入一個新檔案 / 模組前，先用幾句話交代它的**輪廓**，他才知道自己要踏進什麼：

- 它的**職責**是什麼（一句話）。
- 對外 **API 的大致形狀**、提供哪些功能。
- 有哪些**重要的不變式 / 陷阱 / 設計取捨**值得先記住。

這樣讀者進去之後，看到的每個細節都能掛回這個框架，不會散成一地零件。

## 進入一個 function 前：先給一句話

要展開一個重要的呼叫前，先一句話定位它，再深入：**它的目的**、**關鍵參數**（只挑影響主線的）、
**回傳什麼**、**有什麼要注意的**（例如會 mutate、會 fail-fast、有副作用）。讀者帶著這個預期
再看內部，就讀得很順。

## 先講掉「葉子節點」前提，別讓它打斷主線

主線敘事最怕被前提知識岔斷。所以**在開講主線之前**，先把那些「為了聽懂主線必須先知道、
但本身不是主線」的葉子知識用一兩句交代清楚——某個 collaborator 的角色、一個基礎設施 /
schema 的事實、某個元件給你什麼保證。

*例如*：「先知道兩件事就好：`gateway` 是 backend 對外部 IdP 的代理，幫你把『建使用者』
這種呼叫包成一次 API call；`sealer` 給你一個防竄改的信封，封進去的東西別人改不了。
記住這兩個角色，下面主線就不會卡。」

點到為止——目的只是讓主線講得順，不是把前提也講成另一場導覽。

## 修剪無關細節

不是每個細節都值得講。判準是「**對理解主線有沒有幫助**」：

- 與主線無關的實作，只講「它給我什麼」。*例如*：一個亂數密碼產生器，講「它回一組符合
  複雜度規則的亂數密碼」就夠了，不用講它怎麼洗牌、用哪個 charset。
- 可控的參數，若對主線不重要，**連參數都不用提**。
- 如果你發現自己在解釋一段「換成別的寫法也不影響理解」的程式，那多半可以跳過或一句帶過。

留白是一種尊重：把讀者的注意力留給真正承載意圖的地方。

## 邊界

- **只讀、只講，不改 code**。這是導覽，不是重構，也不是 bug review。若沿途看到疑似問題，
  可以一句話標記「這裡看起來怪，要的話另開」，但不要岔進去修或展開檢討。
- **找 bug / 評品質**不是這個 skill 的工作——那是 code review 類技能的事。這裡的成功標準是
  「讀者懂了這段在幹嘛」，不是「挑出幾個缺陷」。
- **用讀者的語言**回覆（中文就中文、英文就英文），技術名詞 / 業界慣用詞保留原文即可。

## 一段好導覽的形狀（示意）

> **總綱**：這趟我們看「登入」怎麼運作，從使用者按下登入到後端發出 token 為止；不看
> 權限與資料層。主線會經過三站：① 入口接線 → ② 換 token → ③ 維持登入。
> 先記住一個前提：`broker` 是後端代替前端跟 IdP 打交道的角色。
>
> **第一站（入口接線）**：…（意圖→目的→後果，標 `main.go:NN`，需要時「跳到 `broker.go:NN`」）…
>
> 這是第一站。要我接著走第二站（換 token），還是這裡先停讓你問？
