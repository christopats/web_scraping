const puppeteer = require("puppeteer");

(async () => {
  try {
    console.log("Launching browser...");
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    console.log("Navigating to Google...");
    await page.goto("https://www.google.com");
    console.log("Closing browser...");
    await browser.close();
    console.log("Done!");
  } catch (error) {
    console.error("An error occurred:", error);
  }
})();
