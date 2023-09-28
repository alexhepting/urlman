package com.example.urlmanager

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import android.widget.Toast

class UrlManager(context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {

    companion object {
        private const val DATABASE_NAME = "urls.db"
        private const val DATABASE_VERSION = 1
    }

    override fun onCreate(db: SQLiteDatabase?) {
        db?.execSQL("CREATE TABLE IF NOT EXISTS urls " +
                "(id INTEGER PRIMARY KEY, " +
                "url TEXT, " +
                "description TEXT, " +
                "category TEXT)")
    }

    override fun onUpgrade(db: SQLiteDatabase?, oldVersion: Int, newVersion: Int) {
        db?.execSQL("DROP TABLE IF EXISTS urls")
        onCreate(db)
    }

    fun addUrl(url: String, description: String, category: String) {
        val db = this.writableDatabase
        val sql = "INSERT INTO urls (url, description, category) VALUES ('$url', '$description', '$category')"
        db.execSQL(sql)
        db.close()
    }

    fun deleteUrl(id: Int) {
        val db = this.writableDatabase
        val sql = "DELETE FROM urls WHERE id=$id"
        db.execSQL(sql)
        db.close()
    }

    fun getUrlsList(): ArrayList<String> {
        val db = this.readableDatabase
        val cursor = db.rawQuery("SELECT * FROM urls", null)
        val list = ArrayList<String>()
        if (cursor.moveToFirst()) {
            do {
                val description = cursor.getString(cursor.getColumnIndex("description"))
                val url = cursor.getString(cursor.getColumnIndex("url"))
                val category = cursor.getString(cursor.getColumnIndex("category"))
                list.add("Description: $description, URL: $url, Category: $category")
            } while (cursor.moveToNext())
        }
        cursor.close()
        db.close()
        return list
    }

    fun validateUrl(url: String): Boolean {
        if (url.isEmpty()) {
            showToast("Please enter a URL.")
            return false
        }
        return true
    }

    fun validateDescription(description: String): Boolean {
        if (description.isEmpty()) {
            showToast("Please enter a description.")
            return false
        }
        return true
    }

    fun validateCategory(category: String): Boolean {
        if (category.isEmpty()) {
            showToast("Please enter a category.")
            return false
        }
        return true
    }

    fun getInsightsData(): Map<String, Int> {
        val db = this.readableDatabase
        val cursor = db.rawQuery("SELECT category, COUNT(*) FROM urls GROUP BY category", null)
        val insightsData = mutableMapOf<String, Int>()
        if (cursor.moveToFirst()) {
            do {
                val category = cursor.getString(0)
                val count = cursor.getInt(1)
                insightsData[category] = count
           
