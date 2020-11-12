import boto3
import re
import sys

client = boto3.client("comprehend")

with open("truth.csv", "r") as fin:
    with open("aws_response.csv", "w") as fout:
        fout.write("ID,Sentiment,Positive,Negative,Neutral,Mixed\n")
        for line in fin:
            idx = line.split(",")[0]
            m = re.match(r"\d+,\d+,b\"?\'?(.*)\"?\'?\n", line)
            if m:
                review = m.group(1)[:-1]

                response = client.detect_sentiment(
                    Text=review,
                    LanguageCode="en"
                )
                if response:
                    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        fout.write(f"{idx},{response['Sentiment']},{response['SentimentScore']['Positive']},{response['SentimentScore']['Negative']},{response['SentimentScore']['Neutral']},{response['SentimentScore']['Mixed']}\n")
                        print(idx)
                    else:
                        print(f"Non-200 code - {idx}")
                else:
                    print(f"No response - {idx}")