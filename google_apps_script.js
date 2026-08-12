// =====================================================================
//  IKON COMPUTER EDUCATION — Google Apps Script
//  Saves internship registrations to Google Sheets (stored in Drive)
// =====================================================================
//
//  ══════════════════════════════════════════════════════════════════
//  SETUP STEPS (Do this ONCE — takes ~5 minutes):
//  ══════════════════════════════════════════════════════════════════
//
//  STEP 1 ─ Create a Google Sheet
//    • Go to https://sheets.google.com
//    • Click  ＋  to create a new blank spreadsheet
//    • Name it:  "Ikon Internship Registrations 2026"
//    • Copy the Sheet ID from the URL:
//        https://docs.google.com/spreadsheets/d/  ← SHEET_ID →  /edit
//    • Paste that ID in SHEET_ID below (replace the placeholder)
//
//  STEP 2 ─ Open Apps Script editor
//    • Inside the same Google Sheet, click:
//        Extensions  →  Apps Script
//    • Delete any existing code in the editor
//    • Paste the ENTIRE contents of this file (below the comments)
//    • Click 💾 Save  (Ctrl+S)
//
//  STEP 3 ─ Deploy as a Web App
//    • Click  Deploy  →  New Deployment
//    • Under "Select type" choose  Web App
//    • Fill in:
//        Description  :  Ikon Registration Handler
//        Execute as   :  Me  (your Google account)
//        Who has access:  Anyone
//    • Click  Deploy
//    • Click  Authorize access  → choose your Google account → Allow
//    • COPY the Web App URL shown (looks like:
//        https://script.google.com/macros/s/AKfycb.../exec )
//
//  STEP 4 ─ Paste the URL into your website
//    • Open  d:\Internshipsite\script.js
//    • Find line:
//        const GOOGLE_SCRIPT_URL = 'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE';
//    • Replace  'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE'
//      with the URL you copied, e.g.:
//        const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycb.../exec';
//    • Save script.js — you're done! ✅
//
//  ══════════════════════════════════════════════════════════════════
//  WHAT GETS SAVED (one row per registration):
//    Timestamp | Name | Email | Phone | Course | Mode | Message
//  ══════════════════════════════════════════════════════════════════

// ── PASTE YOUR GOOGLE SHEET ID HERE ──────────────────────────────
const SHEET_ID = 'YOUR_GOOGLE_SHEET_ID_HERE';
// ─────────────────────────────────────────────────────────────────

const SHEET_NAME = 'Registrations'; // Tab name inside the Sheet

// Column headers (written automatically on first submission)
const HEADERS = [
  'Timestamp (IST)',
  'Full Name',
  'Email Address',
  'Phone Number',
  'Course Selected',
  'Mode Preferred',
  'Message / Query',
];

// ── Friendly course labels ────────────────────────────────────────
const COURSE_LABELS = {
  java:        '☕ Java Programming',
  python:      '🐍 Python Development',
  dbms:        '🗄️ DBMS',
  networking:  '🌐 Computer Networking',
  combo:       '📦 Combo (Multiple Courses)',
};

const MODE_LABELS = {
  online:  '💻 Online',
  offline: '🏫 Offline',
};

// ─────────────────────────────────────────────────────────────────
//  doPost — called when the website submits the form
// ─────────────────────────────────────────────────────────────────
function doPost(e) {
  try {
    // Parse incoming JSON body
    const data = JSON.parse(e.postData.contents);

    const ss    = SpreadsheetApp.openById(SHEET_ID);
    let   sheet = ss.getSheetByName(SHEET_NAME);

    // Create sheet tab if it doesn't exist yet
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
    }

    // Write header row if the sheet is brand new (only 1 row = empty)
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);

      // Style the header row
      const headerRange = sheet.getRange(1, 1, 1, HEADERS.length);
      headerRange.setBackground('#1a73e8')
                 .setFontColor('#ffffff')
                 .setFontWeight('bold')
                 .setFontSize(11);
      sheet.setFrozenRows(1);
    }

    // Append the new registration as a row
    sheet.appendRow([
      data.timestamp   || new Date().toLocaleString('en-IN'),
      data.name        || '',
      data.email       || '',
      data.phone       || '',
      COURSE_LABELS[data.course] || data.course || '',
      MODE_LABELS[data.mode]     || data.mode   || '',
      data.message     || '',
    ]);

    // Auto-resize columns for readability
    sheet.autoResizeColumns(1, HEADERS.length);

    // ── Optional: send notification email to institute ────────────
    // Uncomment the lines below and set your institute email address:
    //
    // MailApp.sendEmail({
    //   to:      'info@ikoncomputer.edu.in',
    //   subject: '🎓 New Internship Registration — ' + (data.name || 'Unknown'),
    //   body:    'New registration received:\n\n' +
    //            'Name    : ' + data.name + '\n' +
    //            'Email   : ' + data.email + '\n' +
    //            'Phone   : ' + data.phone + '\n' +
    //            'Course  : ' + (COURSE_LABELS[data.course] || data.course) + '\n' +
    //            'Mode    : ' + (MODE_LABELS[data.mode] || data.mode) + '\n' +
    //            'Message : ' + data.message + '\n\n' +
    //            'Timestamp: ' + data.timestamp,
    // });

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'success' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ── doGet — health check (visit the URL in browser to confirm live) ──
function doGet() {
  return ContentService
    .createTextOutput('✅ Ikon Registration Script is live and ready.')
    .setMimeType(ContentService.MimeType.TEXT);
}
