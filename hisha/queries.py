SINGLE = '''
query ($search: String, $status: MediaStatus) {
    Media(search: $search, status: $status, type: ANIME) {
        id
        idMal
        episodes
        duration
        popularity
        averageScore
        bannerImage
        coverImage {
            large
        }
        title {
            userPreferred
            native
            english
            romaji
        }
        synonyms
        startDate {
            year
            month
            day
        }
        endDate {
            year
            month
            day
        }
        studios {
            edges {
                isMain
                node {
                    name
                    siteUrl
                }
            }
        }
    }
}
'''

PAGE = '''
query ($search: String, $status: MediaStatus) {
    Page (page: 1) {
        pageInfo {
            total
            currentPage
        }

        media(search: $search, status: $status, type: ANIME) {
            id
            idMal
            episodes
            duration
            popularity
            averageScore
            bannerImage
            coverImage {
                large
            }
            title {
                userPreferred
                native
                english
                romaji
            }
            synonyms
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            studios {
                edges {
                    isMain
                    node {
                        name
                        siteUrl
                    }
                }
            }
        }
    }
}
'''