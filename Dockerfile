# Use Anaconda3 base image
FROM continuumio/anaconda3:4.4.0

# Set the working directory inside the container
WORKDIR /usr/app/

# Copy the current directory contents into the container at /usr/app/
COPY . .

# Update pip to the latest version
RUN python -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
# Use conda for Anaconda specific packages
RUN conda install --yes --file requirements.txt

# Expose port 8080 to the outside world
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "app.py"]

