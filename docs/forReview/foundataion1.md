This guide is designed for the `01-Foundations/readme.md` file. It focuses on the **NIAID Data Discovery Portal**, as it is the most accessible entry point for someone who has never touched an API.

---

# 🟢 Module 1: Foundations of APIs

### *What they are and how to use them without writing a single line of code.*

## 1. What is an API? (The "Librarian" Analogy)

Imagine you are at the **National Library of Medicine**. You want a specific set of clinical trial results.

* **The Database:** This is the massive collection of books in the back room. You aren't allowed to just walk in and start digging through the shelves.
* **The API:** This is the **Librarian**. You walk up to the desk and give them a specific request (e.g., "I need all studies on Malaria from 2023").
* **The Request:** This is the note you hand the librarian.
* **The Response:** The librarian goes into the back, finds exactly what you asked for, and brings it back to you in a neatly organized folder (**JSON**).

---

## 2. Anatomy of an API Call

When we talk to an NIAID API, the "Request" usually looks like a URL. Let’s break down a search for **Zika Virus** data:

`https://api.data.niaid.nih.gov/v1/query?q=zika`

1. **The Base URL:** `https://api.data.niaid.nih.gov/v1/` (The Librarian's desk).
2. **The Endpoint:** `query` (The specific task you want the librarian to do).
3. **The Parameters:** `?q=zika` (The specific details of your request).

---

## 3. Hands-on: Using the Swagger UI

Most NIAID APIs come with a **Swagger UI** (also known as OpenAPI documentation). This is a website that lets you "test drive" the API by clicking buttons instead of writing code.

### Step-by-Step Exercise:

1. **Open the Interface:** Go to the [NIAID Discovery Portal API Docs](https://api.data.niaid.nih.gov/).
2. **Find the "GET" Method:** Look for the green `GET /query` row and click to expand it.
3. **Try it out:** Click the **"Try it out"** button on the right.
4. **Enter Search Terms:** In the `q` field, type `tuberculosis`.
5. **Execute:** Scroll down and hit the big blue **"Execute"** button.

### What just happened?

If you scroll down to the **Server Response**, you will see:

* **Request URL:** The exact URL the tool built for you.
* **Response Body:** A block of text starting with `{`. This is **JSON**. It contains the actual data (titles, authors, and dates) for those TB datasets.

---

## 4. Why does NIAID use JSON?

You might notice the data looks a bit messy at first glance. It uses curly braces `{}` and quotes `""`.

```json
{
  "name": "Tuberculosis Research Study",
  "author": "NIAID Investigator",
  "year": 2024
}

```

**JSON (JavaScript Object Notation)** is the standard because:

1. **It’s Lightweight:** It travels across the NIH network much faster than a heavy Excel file.
2. **It’s Universal:** Every programming language (Python, R, Java) can read it instantly.
3. **It’s Hierarchical:** It can show complex relationships (like a patient linked to multiple lab results) better than a flat spreadsheet.

---

## 🚀 Next Step

Now that you've made your first request, would you like to move to **Module 2: The Integrator**, where we show you how to pull this same data into an **Excel sheet or a Python script** automatically?