import boto3from flask import request, jsonify, Flaskapp = Flask(__name__)# AWS S3 configurations3_client = boto3.client('s3')bucket_name = 'bucket935048'lambda_function_name = 'Assigndocumenttousers'@app.route("/")def hello():    return "Hello"# Endpoint to handle file upload@app.route('/upload', methods=['POST'])def upload_file():    if 'file' not in request.files:        return jsonify({'error': 'No file provided'}), 400    file = request.files['file']    if file.filename == '':        return jsonify({'error': 'No file selected'}), 400    try:        # Upload file to S3 bucket        s3_client.upload_fileobj(file, bucket_name, file.filename)        # Generate pre-signed URL for the uploaded file file_url = s3_client.generate_presigned_url('get_object',        # Params={'Bucket': bucket_name, 'Key': file.filename}, ExpiresIn=3600)        return jsonify({'success': 'file uploaded to s3 bucket successfully'}), 200    except Exception as e:        return jsonify({'error': str(e)}), 500if __name__ == '__main__':    app.run(debug=True)