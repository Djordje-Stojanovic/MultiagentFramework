# Gemini Developer API

Get a Gemini API key and make your first API request in minutes.

### Python

```
from google import genai
client = genai.Client()
response = client.models.generate_content(
model="gemini-2.5-flash",
contents="Explain how AI works in a few words",
)
print(response.text)
```


### JavaScript

```
import { GoogleGenAI } from "@google/genai";
const ai = new GoogleGenAI({});
async function main() {
const response = await ai.models.generateContent({
model: "gemini-2.5-flash",
contents: "Explain how AI works in a few words",
});
console.log(response.text);
}
await main();
```


### Go

```
package main
import (
"context"
"fmt"
"log"
"google.golang.org/genai"
)
func main() {
ctx := context.Background()
client, err := genai.NewClient(ctx, nil)
if err != nil {
log.Fatal(err)
}
result, err := client.Models.GenerateContent(
ctx,
"gemini-2.5-flash",
genai.Text("Explain how AI works in a few words"),
nil,
)
if err != nil {
log.Fatal(err)
}
fmt.Println(result.Text())
}
```


### Java

```
package com.example;
import com.google.genai.Client;
import com.google.genai.types.GenerateContentResponse;
public class GenerateTextFromTextInput {
public static void main(String[] args) {
Client client = new Client();
GenerateContentResponse response =
client.models.generateContent(
"gemini-2.5-flash",
"Explain how AI works in a few words",
null);
System.out.println(response.text());
}
}
```


### REST

```
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" \
-H "x-goog-api-key: $GEMINI_API_KEY" \
-H 'Content-Type: application/json' \
-X POST \
-d '{
"contents": [
{
"parts": [
{
"text": "Explain how AI works in a few words"
}
]
}
]
}'
```


## Meet the models

## Explore the API

### Explore long context

Input millions of tokens to Gemini models and derive understanding from unstructured images, videos, and documents.

### Generate structured outputs

Constrain Gemini to respond with JSON, a structured data format suitable for automated processing.
