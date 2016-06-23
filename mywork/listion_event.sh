#curl's -N flag turns off input buffering which is required to process the stream incrementally.
curl -NsS localhost:8000/events?token="75661625cdf09bd4ca5f29b3a5318241b00db72c"
