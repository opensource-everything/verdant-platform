import os, secrets, time, sqlite3, base64


store_struct = [


    # Landscape Fact Tables

    {
        'table_name':'dim_filename',
        'attributes':'''
            file_key INTEGER PRIMARY KEY,
            filename_id TEXT,
            filename TEXT,
            encoded_bytes TEXT,
            path_id TEXT,
            file_byte_ids TEXT,
            thumbnail_byte_ids TEXT
        '''
    },

    {
        'table_name':'dim_file_bytes',
        'attributes':'''
            file_byte_key INTEGER PRIMARY KEY,
            file_byte_id TEXT,
            file_byte TEXT
        '''
    },

    {
        'table_name':'dim_path',
        'attributes':'''
            expense_key INTEGER PRIMARY KEY,
            expense_id TEXT,
            item_id TEXT,
            timestamp_id TEXT
        '''
    },

    
]


'''
Images encoding into base64
Prepping images for HTML injection
'''
def encode_image_files(image_list):
    image_data = []
    for i, image in enumerate(image_list):
        print(f'Encoding image {i}/{len(image_list)}')
        print(image)

        with open(image, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            _, ext = os.path.splitext(image)

            if ext == '.jpeg' or '.jpg':
                new_string = f'data:image/jpeg;base64,{img_base64}'
            elif ext == '.png':
                new_string = f'data:image/png;base64,{img_base64}'
            elif ext == '.bmp':
                new_string = f'data:image/bmp;base64,{img_base64}'

        image_data.append(new_string)

    return image_data


# Create all tables defined in store_struct
def generate_inner_files(folders):
	allowed_ext = ['.jpeg', '.jpg', '.png', '.bmp']
	for folder in folders:
		for r,s,f in os.walk(folder):
			for _ in f:
				filename, file_ext = os.path.splitext(os.path.join(r,_))
				if file_ext.lower() in allowed_ext:
					yield os.path.join(r, _)

def create_table_string(table_name, table_attrs):
    return f'''CREATE TABLE IF NOT EXISTS {table_name} ( {table_attrs} )'''

# 
# Create all tables defined in store_struct
# 
def table_digest(c):
    for t in store_struct:

        table_name = t['table_name']
        attrs = t['attributes']
        # print(table_name, attrs)

        table_string = create_table_string(table_name, attrs)
        c.execute(table_string)



def construct_insert_statement(table_name, table_attrs):
    qmarks = ['?' for x in range(len(table_attrs))] 
    marks = f"({', '.join(qmarks)})"
    attrs = f"({', '.join(table_attrs)})"
    tuple_attrs = tuple(table_attrs)
    
    sql_statement = f'INSERT INTO {table_name} {attrs} VALUES {marks}'
    return sql_statement

def generate_random_hash(length):
    return secrets.token_hex(length // 2)



def create_tables(db_filename):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()

    table_digest(c)
    conn.commit()
    conn.close()

def insert_filenames(db_filename, filenames, file_bytes):
	conn = sqlite3.connect(db_filename)
	c = conn.cursor()

	file_schema = zip(filenames, file_bytes)


	# created_at_unix = time.time()
	# construct_insert_statement()

	for fn, fb in file_schema:
		file_id = generate_random_hash(12)
		c.execute("INSERT INTO dim_filename (filename, filename_id, encoded_bytes) VALUES (?,?,?)", (fn, file_id, fb))

	conn.commit()
	conn.close()


def main():
	folders = [
	r'H:\archives\Laptop\2024\FEB\DL\304s',
	r'H:\archives\Laptop\2024\JAN\DOWNLOAD\304',
	r'H:\archives\Laptop\2023\MAY\Day 29 May 08_27_17 AM\Downloads\304',
	r'H:\archives\Laptop\2023\304',
	r'H:\archives\Laptop\2023\MAY\304',
	r'H:\archives\Laptop\2023\304 Dup',
	r'H:\archives\Laptop\2023\304 Dups',
	r'H:\archives\Laptop\2023\304s',
	r'H:\archives\Laptop\2024\304s',
	r'H:\archives\Laptop\2024\304'
	]

	filenames_consolidated = [f for f in generate_inner_files(folders)]
	print(filenames_consolidated)
	file_bytes = encode_image_files(filenames_consolidated)



	print(filenames_consolidated)
	create_tables('file_tagging_app.db')
	insert_filenames('file_tagging_app.db', filenames_consolidated, file_bytes)




if __name__ == '__main__':
	main()