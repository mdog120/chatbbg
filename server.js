import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import OpenAI from "openai";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

app.post("/api/chat", async (req, res) => {
  try {
    const { messages } = req.body;

    // basic validation
    if (!Array.isArray(messages)) {
      return res.status(400).json({ error: "messages must be an array" });
    }

    const completion = await client.chat.completions.create({
      model: "gpt-4.1-mini",
      messages,
      temperature: 0.8,
    });

    const reply = completion.choices?.[0]?.message?.content ?? "";
    res.json({ reply });
  } catch (err) {
    console.error(err);
    res.status(500).send(err?.message || "Server error");
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`ChatBBG running on http://localhost:${PORT}`));
