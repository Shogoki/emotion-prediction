FROM tensorflow/serving:1.13.0
 
COPY ./models/tf /models

EXPOSE 8501

ENV MODEL_NAME=model
#docker run -t --rm -p 8501:8501 \
#    -v "$TESTDATA/saved_model_half_plus_two_cpu:/models/half_plus_two" \
#    -e MODEL_NAME=half_plus_two \
#    tensorflow/serving &
