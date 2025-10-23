package com.mpumpcalc.app;

import android.Manifest;
import android.app.DownloadManager;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.CancellationSignal;
import android.os.Environment;
import android.os.ParcelFileDescriptor;
import android.print.PageRange;
import android.print.PrintAttributes;
import android.print.PrintDocumentAdapter;
import android.print.PrintDocumentInfo;
import android.print.PrintManager;
import android.provider.MediaStore;
import android.util.Base64;
import android.webkit.CookieManager;
import android.webkit.DownloadListener;
import android.webkit.JavascriptInterface;
import android.webkit.URLUtil;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import android.provider.MediaStore;



public class MainActivity extends AppCompatActivity {

    private WebView webView;
    private static final int PERMISSION_REQUEST_CODE = 100;
    private static final int PDF_PERMISSION_REQUEST_CODE = 101;
    private static final String APP_URL = "https://mupro-alpha.vercel.app/"; // Change to your deployed URL
    
    // Store pending PDF data when waiting for permissions
    private String pendingPdfBase64 = null;
    private String pendingPdfFileName = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Request permissions
        checkPermissions();

        // Initialize WebView
        webView = findViewById(R.id.webview);
        setupWebView();

        // Load app
        webView.loadUrl(APP_URL);
    }
    // Add this method inside your MainActivity class

    private void checkPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED ||
                    ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {

                // Permissions are not granted, so request them.
                ActivityCompat.requestPermissions(this,
                        new String[]{
                                Manifest.permission.WRITE_EXTERNAL_STORAGE,
                                Manifest.permission.READ_EXTERNAL_STORAGE
                        },
                        PERMISSION_REQUEST_CODE);
            }
        }
        // For Android versions below M (Marshmallow), permissions are granted at install time,
        // so no runtime check is needed.
    }

    private void setupWebView() {
        WebSettings webSettings = webView.getSettings();
        
        // Enable JavaScript
        webSettings.setJavaScriptEnabled(true);
        
        // Add JavaScript Interface for PDF handling
        webView.addJavascriptInterface(new PdfJavaScriptInterface(this), "MPumpCalcAndroid");
        
        // Enable DOM Storage for localStorage
        webSettings.setDomStorageEnabled(true);
        
        // Enable Database
        webSettings.setDatabaseEnabled(true);

        // Enable Zoom
        webSettings.setSupportZoom(true);
        webSettings.setBuiltInZoomControls(false);
        webSettings.setDisplayZoomControls(false);
        
        // Enable viewport
        webSettings.setUseWideViewPort(true);
        webSettings.setLoadWithOverviewMode(true);
        
        // Enable file access
        webSettings.setAllowFileAccess(true);
        webSettings.setAllowContentAccess(true);
        
        // Mixed content mode
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            webSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        }
        
        // Set User Agent
        String userAgent = webSettings.getUserAgentString();
        webSettings.setUserAgentString(userAgent + " MPumpCalc/1.0");
        
        // WebView Client
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                // Inject CSS to hide any unwanted elements if needed
            }
        });
        
        // WebChrome Client for alerts, confirm, etc
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                super.onProgressChanged(view, newProgress);
                // You can add a progress bar here
            }
        });
        
        // Download Listener for PDF downloads
        webView.setDownloadListener(new DownloadListener() {
            @Override
            public void onDownloadStart(String url, String userAgent, String contentDisposition,
                                        String mimeType, long contentLength) {
                downloadFile(url, userAgent, contentDisposition, mimeType);
            }
        });
    }

    private void downloadFile(String url, String userAgent, String contentDisposition, String mimeType) {
        try {
            DownloadManager.Request request = new DownloadManager.Request(Uri.parse(url));
            request.setMimeType(mimeType);
            
            String cookies = CookieManager.getInstance().getCookie(url);
            request.addRequestHeader("cookie", cookies);
            request.addRequestHeader("User-Agent", userAgent);
            
            request.setDescription("Downloading file...");
            request.setTitle(URLUtil.guessFileName(url, contentDisposition, mimeType));
            
            request.allowScanningByMediaScanner();
            request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
            request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS,
                    URLUtil.guessFileName(url, contentDisposition, mimeType));
            
            DownloadManager dm = (DownloadManager) getSystemService(DOWNLOAD_SERVICE);
            dm.enqueue(request);
            
            Toast.makeText(getApplicationContext(), "Downloading...", Toast.LENGTH_SHORT).show();
        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(getApplicationContext(), "Download failed", Toast.LENGTH_SHORT).show();
        }
    }
    private void openPdfFileWithUri(Uri uri) {
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.setDataAndType(uri, "application/pdf");
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NO_HISTORY);

        try {
            startActivity(intent);
        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(this, "No application available to view PDF", Toast.LENGTH_SHORT).show();
        }
    }



    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        
        if (requestCode == PDF_PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permission granted, save pending PDF
                if (pendingPdfBase64 != null && pendingPdfFileName != null) {
                    Toast.makeText(this, "Permission granted! Saving PDF...", Toast.LENGTH_SHORT).show();
                    
                    // Create interface and save PDF
                    PdfJavaScriptInterface pdfInterface = new PdfJavaScriptInterface(this);
                    pdfInterface.savePdfFile(pendingPdfBase64, pendingPdfFileName);

                    // Clear pending data
                    pendingPdfBase64 = null;
                    pendingPdfFileName = null;
                }
            } else {
                // Permission denied
                Toast.makeText(this, "Permission denied. Cannot save PDF without storage permission.", 
                        Toast.LENGTH_LONG).show();
                pendingPdfBase64 = null;
                pendingPdfFileName = null;
            }
        }
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        webView.onResume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        webView.onPause();
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.destroy();
        }
        super.onDestroy();
    }

    // JavaScript Interface for PDF handling
    public class PdfJavaScriptInterface {
        Context context;

        PdfJavaScriptInterface(Context c) {
            context = c;
        }

        @JavascriptInterface
        public boolean hasStoragePermission() {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                return ContextCompat.checkSelfPermission(context, Manifest.permission.WRITE_EXTERNAL_STORAGE)
                        == PackageManager.PERMISSION_GRANTED;
            }
            return true; // Pre-M permissions are granted at install time
        }

        @JavascriptInterface
        public void requestStoragePermission() {
            runOnUiThread(() -> {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    ActivityCompat.requestPermissions(MainActivity.this,
                            new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE,
                                    Manifest.permission.READ_EXTERNAL_STORAGE},
                            PDF_PERMISSION_REQUEST_CODE);
                }
            });
        }

        @JavascriptInterface
        public void printPdf(String base64Pdf, String fileName) {
            try {
                // Decode base64 to bytes
                byte[] pdfBytes = Base64.decode(base64Pdf, Base64.DEFAULT);
                
                // Save to cache (temporary file)
                File cacheDir = context.getCacheDir();
                File pdfFile = new File(cacheDir, fileName);
                
                FileOutputStream fos = new FileOutputStream(pdfFile);
                fos.write(pdfBytes);
                fos.close();
                
                // Open Android Print Dialog
                runOnUiThread(() -> {
                    printPdfFile(pdfFile, fileName);
                });
                
            } catch (IOException e) {
                e.printStackTrace();
                runOnUiThread(() -> {
                    Toast.makeText(context, "Failed to prepare PDF for printing", Toast.LENGTH_SHORT).show();
                });
            }
        }

        private void printPdfFile(File pdfFile, String jobName) {
            // Get PrintManager
            PrintManager printManager = (PrintManager) context.getSystemService(Context.PRINT_SERVICE);
            
            if (printManager != null) {
                // Create print document adapter
                PrintDocumentAdapter printAdapter = new PdfPrintDocumentAdapter(pdfFile, jobName);
                
                // Start print job
                printManager.print(jobName, printAdapter, null);
                
                Toast.makeText(context, "Opening print dialog...", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(context, "Print service not available", Toast.LENGTH_SHORT).show();
            }
        }

        @JavascriptInterface
        public void openPdfWithViewer(String base64Pdf, String fileName) {
            // No permission check is needed here anymore for saving.
            // Directly call the save method.
            savePdfFile(base64Pdf, fileName);
        }


        // Permission granted, save PDF


        private void savePdfFile(String base64Pdf, String fileName) {
            try {
                byte[] pdfBytes = Base64.decode(base64Pdf, Base64.DEFAULT);

                ContentResolver resolver = context.getContentResolver();
                ContentValues contentValues = new ContentValues();
                contentValues.put(MediaStore.MediaColumns.DISPLAY_NAME, fileName);
                contentValues.put(MediaStore.MediaColumns.MIME_TYPE, "application/pdf");

                // Save to the Downloads folder
                contentValues.put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS);

                Uri pdfUri = resolver.insert(MediaStore.Files.getContentUri("external"), contentValues);

                if (pdfUri != null) {
                    try (OutputStream os = resolver.openOutputStream(pdfUri)) {
                        if (os != null) {
                            os.write(pdfBytes);
                        }
                    }

                    runOnUiThread(() -> {
                        Toast.makeText(context, "PDF saved to Downloads: " + fileName, Toast.LENGTH_LONG).show();
                    });

                    // You can still call openPdfFile if you want to immediately view it
                    openPdfFileWithUri(pdfUri);

                } else {
                    throw new IOException("Failed to create new MediaStore record.");
                }

            } catch (IOException e) {
                e.printStackTrace();
                runOnUiThread(() -> {
                    Toast.makeText(context, "Failed to save PDF: " + e.getMessage(), Toast.LENGTH_LONG).show();
                });
            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() -> {
                    Toast.makeText(context, "An error occurred: " + e.getMessage(), Toast.LENGTH_LONG).show();
                });
            }
        }


        private void openPdfFile(File file) {
            Uri uri;
            
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                // For Android 7.0+ use FileProvider
                uri = FileProvider.getUriForFile(
                        context,
                        context.getApplicationContext().getPackageName() + ".fileprovider",
                        file
                );
            } else {
                uri = Uri.fromFile(file);
            }
            
            Intent intent = new Intent(Intent.ACTION_VIEW);
            intent.setDataAndType(uri, "application/pdf");
            intent.setFlags(Intent.FLAG_ACTIVITY_NO_HISTORY);
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            
            // Create chooser to show "Open with..." dialog
            Intent chooser = Intent.createChooser(intent, "Open PDF with");
            
            try {
                context.startActivity(chooser);
            } catch (Exception e) {
                runOnUiThread(() -> {
                    Toast.makeText(context, "No PDF viewer found. Please install a PDF reader app.", Toast.LENGTH_LONG).show();
                });
            }
        }
    }

    // Print Document Adapter for PDF
    private class PdfPrintDocumentAdapter extends PrintDocumentAdapter {
        private File pdfFile;
        private String jobName;

        PdfPrintDocumentAdapter(File pdfFile, String jobName) {
            this.pdfFile = pdfFile;
            this.jobName = jobName;
        }

        @Override
        public void onLayout(PrintAttributes oldAttributes, PrintAttributes newAttributes,
                           CancellationSignal cancellationSignal, LayoutResultCallback callback,
                           Bundle extras) {
            if (cancellationSignal.isCanceled()) {
                callback.onLayoutCancelled();
                return;
            }

            PrintDocumentInfo info = new PrintDocumentInfo.Builder(jobName)
                    .setContentType(PrintDocumentInfo.CONTENT_TYPE_DOCUMENT)
                    .setPageCount(PrintDocumentInfo.PAGE_COUNT_UNKNOWN)
                    .build();

            callback.onLayoutFinished(info, true);
        }

        @Override
        public void onWrite(PageRange[] pages, ParcelFileDescriptor destination,
                          CancellationSignal cancellationSignal, WriteResultCallback callback) {
            try {
                FileInputStream input = new FileInputStream(pdfFile);
                FileOutputStream output = new FileOutputStream(destination.getFileDescriptor());

                byte[] buffer = new byte[8192];
                int bytesRead;

                while ((bytesRead = input.read(buffer)) != -1) {
                    if (cancellationSignal.isCanceled()) {
                        callback.onWriteCancelled();
                        input.close();
                        output.close();
                        return;
                    }
                    output.write(buffer, 0, bytesRead);
                }

                input.close();
                output.close();

                callback.onWriteFinished(new PageRange[]{PageRange.ALL_PAGES});

            } catch (IOException e) {
                e.printStackTrace();
                callback.onWriteFailed(e.getMessage());
            }
        }
    }
}