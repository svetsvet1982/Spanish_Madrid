// node html2pdf.js in1.html out1.pdf [in2.html out2.pdf ...]
const { chromium } = require('playwright');
(async () => {
  const a = process.argv.slice(2); const b = await chromium.launch();
  for (let i = 0; i < a.length; i += 2) {
    const pg = await b.newPage();
    await pg.goto('file://' + a[i], { waitUntil: 'networkidle', timeout: 120000 }).catch(() => {});
    await pg.evaluate(() => document.fonts.ready);
    await pg.pdf({ path: a[i + 1], format: 'A4', printBackground: true, displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: '<div style="width:100%;text-align:center;font-size:8pt;color:#777"><span class="pageNumber"></span></div>',
      margin: { top: '18mm', bottom: '18mm', left: '17mm', right: '17mm' } });
    await pg.close(); console.log(a[i + 1]);
  }
  await b.close();
})();
