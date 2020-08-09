# TAXIDI API DOCUMENTATION

## Status Codes

returns the following status codes in its API:

| Status Code | Description             |
| :---------- | :---------------------- |
| 200         | `OK`                    |
| 204         | `No Content`            |
| 400         | `BAD REQUEST`           |
| 401         | `Unauthorized`          |
| 404         | `NOT FOUND`             |
| 500         | `INTERNAL SERVER ERROR` |

## Responses

returns a JSON response in the following format:

```javascript
{
  "body" : string
}
```

The `body` attribute contains all data associated with the response.

## API

**1. Get reviews**

```http
GET /reviews/{id}
```

| Parameter | Type     | Description                    |
| :-------- | :------- | :----------------------------- |
| `id`      | `string` | **Required**. Advertisement id |

Returned JSON:

| Parameter | Description                | Possible Types   |
| :-------- | :------------------------- | :--------------- |
| `body`    | list of associated reviews | `list of string` |

**2. Create a review**

```http
POST /review
```

Body

| Parameter         | Type     | Description                    |
| :---------------- | :------- | :----------------------------- |
| `advertisementID` | `string` | **Required**. Advertisement id |
| `bookingID`       | `string` | **Required**. Booking id       |
| `rating`          | `float`  | **Required**. Rating of review |
| `review`          | `string` | **Required**. Review           |
| `reviewer`        | `string` | **Required**. Reviewer's email |

Returned JSON:

| Parameter | Description     | Possible Types |
| :-------- | :-------------- | :------------- |
| `body`    | success message | `string`       |

**3. Create an advertisement**

**4. Update an advertisement**

```http
PUT /advertisement
```

Body

| Parameter     | Type     | Description                                |
| :------------ | :------- | :----------------------------------------- |
| `id`          | `string` | **Required**. Advertisement id             |
| `title`       | `string` | **Required**. Title of advertisement       |
| `rent`        | `float`  | **Required**. Rental                       |
| `description` | `string` | **Required**. Description of advertisement |

Returned JSON:

| Parameter | Description     | Possible Types |
| :-------- | :-------------- | :------------- |
| `body`    | success message | `string`       |

**5. Delete an advertisement**

**6. Get advertisements**

```http
GET /getAdvertisements/{emial}
```

PATH

| Parameter | Type     | Description              |
| :-------- | :------- | :----------------------- |
| `email`   | `string` | **Required**. user email |

Returned JSON:

| Parameter   | Description                | Possible Types          |
| :---------- | :------------------------- | :---------------------- |
| `body`      | list of associated ads     | `list of advertisements`|

**7. Create a booking**

```http
POST /booking
```

Body

| Parameter         | Type     | Description                                          |
| :---------------- | :------- | :--------------------------------------------------- |
| `advertisementID` | `string` | **Required**. Advertisement id                       |
| `email`           | `string` | **Required**. tenant's email                         |
| `from`            | `string` | **Required**. start date of booking (ex. 20-05-2020) |
| `to`              | `string` | **Required**. end date of booking (ex. 22-05-2020)   |

Returned BODY JSON:

| Parameter   | Description | Possible Types |
| :---------- | :---------- | :------------- |
| `bookingID` | booking id  | `string`       |

**8. Delete a booking**

```http
DELETE /booking/{id}
```

PATH

| Parameter | Type     | Description              |
| :-------- | :------- | :----------------------- |
| `id`      | `string` | **Required**. booking id |

Returned JSON:

`None`

**9. Cancel a booking**

```http
POST /cancelbooking
```

Returned JSON:

| Parameter | Type     | Description                      |
| :-------- | :------- | :------------------------------- |
| `body`    | `string` | **Required**. successful message |

Returned JSON:

`None`

**10. Search Algolia records**

```http
GET /search/{city}
```

PATH

| Parameter | Type     | Description              |
| :-------- | :------- | :----------------------- |
| `city`   | `string` | **Required**. property city |

Returned JSON:

| Parameter   | Description                | Possible Types          |
| :---------- | :------------------------- | :---------------------- |
| `body`      | list of associated ads ids     | `list of advertisements ids`|

**11. Get average review**

```http
GET /avgReviews/{id}
```

PATH

| Parameter | Type     | Description              |
| :-------- | :------- | :----------------------- |
| `id`   | `string` | **Required**. advertisement id |

Returned JSON:

| Parameter   | Description                | Possible Types          |
| :---------- | :------------------------- | :---------------------- |
| `body`      | the average review of an advertisement    | `integer and float`|

**12. Get single advertisement**

## Deploy the sample application

`sh deploy.sh`
