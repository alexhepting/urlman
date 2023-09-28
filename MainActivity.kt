package com.example.urlmanager

import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_main.*
import java.io.File

class MainActivity : AppCompatActivity() {

    private lateinit var urlManager: UrlManager
    private lateinit var adapter: ArrayAdapter<String>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize UrlManager
        urlManager = UrlManager(this)

        // Set up ListView and adapter
        adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, urlManager.getUrlsList())
        urlList.adapter = adapter

        // Set up buttons
        addUrlButton.setOnClickListener {
            val url = urlEntry.text.toString()
            val description = descriptionEntry.text.toString()
            val category = categoryEntry.text.toString()

            if (urlManager.validateUrl(url) && urlManager.validateDescription(description) && urlManager.validateCategory(category)) {
                urlManager.addUrl(url, description, category)
                updateList()
                clearFields()
            }
        }

        deleteSelectedButton.setOnClickListener {
            val selectedPosition = urlList.checkedItemPosition
            if (selectedPosition != -1) {
                urlManager.deleteUrl(selectedPosition)
                updateList()
            }
        }

        exportCsvButton.setOnClickListener {
            showExportDialog(ExportType.CSV)
        }

        exportJsonButton.setOnClickListener {
            showExportDialog(ExportType.JSON)
        }

        exportXmlButton.setOnClickListener {
            showExportDialog(ExportType.XML)
        }

        showInsightsButton.setOnClickListener {
            val insightsData = urlManager.getInsightsData()
            if (insightsData.isNotEmpty()) {
                val dialogBuilder = AlertDialog.Builder(this)
                dialogBuilder.setTitle("Category Distribution")
                val insightsString = insightsData.map { (category, count) -> "$category: $count" }.joinToString("\n")
                dialogBuilder.setMessage(insightsString)
                dialogBuilder.setPositiveButton("OK") { dialog, _ ->
                    dialog.dismiss()
                }
                dialogBuilder.show()
            } else {
                Toast.makeText(this, "No data available for insights.", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun updateList() {
        adapter.clear()
        adapter.addAll(urlManager.getUrlsList())
    }

    private fun clearFields() {
        urlEntry.text.clear()
        descriptionEntry.text.clear()
        categoryEntry.text.clear()
    }

    private fun showExportDialog(exportType: ExportType) {
        val dialogBuilder = AlertDialog.Builder(this)
        dialogBuilder.setTitle("Export")
        dialogBuilder.setMessage("Enter the file name:")

        val fileNameEntry = EditText(this)
        dialogBuilder.setView(fileNameEntry)

        dialogBuilder.setPositiveButton("Export") { dialog, _ ->
            val fileName = fileNameEntry.text.toString()
            if (fileName.isNotEmpty()) {
                val exported = when (exportType) {
                    ExportType.CSV -> urlManager.exportCsv("$fileName.csv")
                    ExportType.JSON -> urlManager.exportJson("$fileName.json")
                    ExportType.XML -> urlManager.exportXml("$fileName.xml")
                }
                if (exported) {
                    Toast.makeText(this, "Export successful", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this, "Export failed", Toast.LENGTH_SHORT).show()
                }
            }
            dialog.dismiss()
        }

        dialogBuilder.setNegativeButton("Cancel") { dialog, _ ->
            dialog.dismiss()
        }

        dialogBuilder.show()
    }
}
