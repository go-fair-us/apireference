package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

func main() {
	http.HandleFunc("/api/datasets/", datasetHandler)
	fmt.Println("Server listening on port 8080")
	http.ListenAndServe(":8080", nil)
}

func datasetHandler(w http.ResponseWriter, r *http.Request) {
	id := strings.TrimPrefix(r.URL.Path, "/api/datasets/")
	filePath := fmt.Sprintf("data/%s.json", id)

	data, err := ioutil.ReadFile(filePath)
	if err != nil {
		http.NotFound(w, r)
		return
	}

	w.Header().Set("Content-Type", "application/ld+json")
	w.Write(data)
}
