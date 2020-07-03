package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"strings"

	"github.com/labstack/echo"

	"github.com/PuerkitoBio/goquery"
)

// Music type
type Music struct {
	Aircheck string `json:"aircheck"`
	Live     string `json:"live"`
}

// SongInfo type
type SongInfo struct {
	Thumbnail string
	Music     Music
}

// Song type
type Song struct {
	ID        string `json:"id"`
	KORTitle  string `json:"kor_title"`
	ENGTitle  string `json:"eng_title"`
	Thumbnail string `json:"thumbnail"`
	Music     Music  `json:"music"`
}

const namuWikiBaseURL string = "https://namu.wiki/w/%EB%8F%99%EB%AC%BC%EC%9D%98%20%EC%88%B2%20%EC%8B%9C%EB%A6%AC%EC%A6%88/%EB%85%B8%EB%9E%98%20%EB%AA%A9%EB%A1%9D"
const nookBaseURL string = "https://nookipedia.com"

func generateRandomID(length int) string {
	var letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	b := make([]byte, length)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}

func getInfo(engTitle string, c chan SongInfo) {
	fmt.Println("[main.go] Scrapping ", engTitle, " from nookipedia...")

	// Create Nook URL
	url := nookBaseURL + "/wiki/" + strings.Replace(engTitle, " ", "_", -1)

	// Request Nook Response
	res, err := http.Get(url)
	checkErr(err)
	checkStatus(res)
	defer res.Body.Close()

	// Load the HTML document
	doc, err := goquery.NewDocumentFromReader(res.Body)
	checkErr(err)

	table := doc.Find(".infobox")
	trs := table.Find("tr")

	// Get aircheck and live flac source
	aircheck, _ := trs.Eq(7).Find("audio").Attr("src")
	live, _ := trs.Eq(9).Find("audio").Attr("src")
	// Get Thumbnail
	imgSrcStr, _ := trs.Eq(5).Find(".image").Find("img").Attr("srcset")
	thumbnail := strings.Split(imgSrcStr, " ")[2]

	music := Music{Aircheck: aircheck, Live: live}
	songInfo := SongInfo{Thumbnail: thumbnail, Music: music}

	// Send songInfo through channel
	c <- songInfo
}

// Check if given rune is japanese
func isJapanese(char rune) bool {
	if 12353 <= int(char) && int(char) <= 12543 {
		return true
	}
	return false
}

// Extract korea title from kor/jpn/eng string
func extractKorTitle(titleStr string) string {
	// If titleStr has [1] footnote anchor
	if strings.Contains(titleStr, "[") {
		return strings.Split(titleStr, "[")[0]
	}
	// Split by first japanese rune
	var splitter string
	for _, char := range titleStr {
		if isJapanese(char) {
			splitter = string(char)
			break
		}
	}
	return strings.Split(titleStr, splitter)[0]
}

// Get song information
func getSongs() []Song {
	// Song array
	var songs []Song

	// Request the HTML page
	res, err := http.Get(namuWikiBaseURL)
	checkErr(err)
	checkStatus(res)
	defer res.Body.Close()

	// Load the HTML document
	doc, err := goquery.NewDocumentFromReader(res.Body)
	checkErr(err)

	// Get the song table
	var songTable *goquery.Selection
	doc.Find(".wiki-table").Each(func(i int, s *goquery.Selection) {
		// For each item found get the fifth table
		if i == 5 {
			songTable = s
		}
	})

	// Channel to receive songInfo
	infoChannel := make(chan SongInfo)

	// Get 96 song title "tr" elements
	songTable.Find("tr").Each(func(i int, s *goquery.Selection) {
		if 1 <= i && i < 96 {
			titleTd := s.Find("td").Slice(1, 2)
			titleDiv := titleTd.Find(".wiki-paragraph")
			korTitle := extractKorTitle(titleDiv.First().Text())
			engTitle := titleDiv.Find(".wiki-size").Last().Text()

			// Go routine for scrapping nookipedia with engTitle
			go getInfo(engTitle, infoChannel)
			// Info receiving channel
			info := <-infoChannel

			// Get all spans in "tr" element
			song := Song{
				ID:        "_" + generateRandomID(10),
				KORTitle:  korTitle,
				ENGTitle:  engTitle,
				Thumbnail: info.Thumbnail,
				Music:     info.Music,
			}

			songs = append(songs, song)
		}
	})

	return songs
}

// Check error
func checkErr(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

// Check response status code
func checkStatus(res *http.Response) {
	if res.StatusCode != 200 {
		log.Fatalf("[Status Code Error] %d %s", res.StatusCode, res.Status)
	}
}

func main() {
	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		songs := getSongs()
		songsJSON, err := json.Marshal(songs)
		checkErr(err)
		return c.String(http.StatusOK, string(songsJSON))
	})
	e.Logger.Fatal(e.Start(":"))
}
