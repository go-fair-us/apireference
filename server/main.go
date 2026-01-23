package main

import (
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	http.HandleFunc("/api/datasets/", handleDataset)
	log.Println("Server listening on port 8080")
	http.ListenAndServe(":8080", nil)
}

func handleDataset(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", 405)
		return
	}

	id := strings.TrimPrefix(r.URL.Path, "/api/datasets/")
	if strings.Contains(id, "..") {
		http.NotFound(w, r)
		return
	}

	filePath := filepath.Join("data", id+".json")
	absData, _ := filepath.Abs("data")
	absFile, _ := filepath.Abs(filePath)
	if !strings.HasPrefix(absFile, absData) {
		http.NotFound(w, r)
		return
	}

	data, err := os.ReadFile(filePath)
	if err != nil {
		log.Printf("Error reading file %s: %v", filePath, err)
		http.NotFound(w, r)
		return
	}

	w.Header().Set("Content-Type", "application/ld+json")
	_, err = w.Write(data)
	if err != nil {
		log.Printf("Error writing response: %v", err)
	}
}
