const puppeteer = require("puppeteer");
const fs = require("fs");

(async () => {
  try {
    console.log("Launching browser...");
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });
    await page.setUserAgent(
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    );

    console.log("Navigating to healthline...");
    await page.goto("https://www.healthline.com/");

    try {
      console.log("Checking for cookies terms popup...");
      await page.waitForSelector(".css-1gdbdla", { timeout: 5000 });
      console.log("Accepting cookies terms...");
      await page.click(".css-1gdbdla");
    } catch (err) {
      console.log("Cookies terms popup not found or already accepted.");
    }

    console.log("Clicking search button...");
    await page.click(".css-6fmqbr");

    // console.log("Waiting for search input...");
    // await page.waitForSelector(".autocomplete");

    console.log("Typing in search term...");
    await page.type("input", "collagen");

    console.log("Submitting search...");
    await page.keyboard.press("Enter");

    console.log("Waiting for search results...");
    await page.waitForSelector("a");

    console.log("Extracting search result links...");
    const searchResultLinks = await page.$$eval("a", (links) =>
      links.map((link) => link.href)
    );

    if (searchResultLinks === null) {
      console.log("Search result not found.");
    } else {
      console.log(
        `Found ${searchResultLinks.length} results. Processing each result...`
      );
    }
    const articles = [];

    for (const [index, link] of searchResultLinks.entries()) {
      console.log(
        `Processing result ${index + 1}/${searchResultLinks.length}: ${link}`
      );
      try {
        console.log("Navigating to article...");
        await page.goto(link, { waitUntil: "networkidle2" });

        // console.log("Waiting for article title...");
        // await page.waitForSelector("h1");

        // console.log("Waiting for article body...");
        // await page.waitForSelector(".css-1avyp1d");

        const title = await page.$eval("h1", (el) => el.textContent);
        const bodyText = await page.$$eval(".css-1avyp1d > p", (paragraphs) =>
          paragraphs.map((p) => p.textContent).join("\n")
        );

        articles.push({ title, bodyText });

        console.log("Article processed. Going back to search results...");
        await page.goBack({ waitUntil: "networkidle2" });
      } catch (err) {
        console.log(`Failed to process result ${index + 1}:`);
      }
    }

    console.log("All articles processed. Writing to file...");

    // Write the articles data to a JSON file
    fs.writeFileSync(
      "articles.json",
      JSON.stringify(articles, null, 2),
      "utf-8"
    );

    await browser.close();
  } catch (error) {
    console.error("An error occured:", error);
  }
})();
