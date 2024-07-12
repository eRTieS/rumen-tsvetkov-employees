DATE_FORMATS = [
    '%d-%m-%Y', '%d-%b-%Y', '%d-%B-%Y', '%m-%d-%Y', '%b-%d-%Y', '%B-%d-%Y', '%Y-%m-%d', '%Y-%b-%d', '%Y-%B-%d'
]

DATE_REGEX = r'([A-Za-z0-9]+)\W{,3}([A-Za-z0-9]+)\W{,3}([A-Za-z0-9]+)'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
