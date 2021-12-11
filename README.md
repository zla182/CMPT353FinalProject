# CMPT 353 Final Project

### Install Packages in the Computer Prompt

* pip install folium
* pip install pillow
* pip install exifread
* pip install GPSphoto
* pip install piexif

### Please download these libraries first

* GPSphoto
* Pandas
* Numpy
* math

### Run the Project

Please use the command below the run the project and given order.

* python hotel_selection.py photos/DT1.jpg
* python recommendedPath.py 13358 Photos/DT1.jpg

For chain_res_distribution.ipynb directly run without command.

### Note

1. Please be sure to transfer photos via usb cable or U disk! If you use discord or messenger to transfer, the geographic location of the photo will be lost, resulting in reading errors!



2. The hotel_selection.py will generate a hotel_list file and an amenities_near_hotel.html file. The hotel_list file includes the hotel information near the current location of the visitor. The amenities_near_hotel.html file shows the location of the hotel and nearby facilities on the map. In the command, the first parameter is the photos from the photos folder, and the second parameter is the file used to save the hotel list. If the program shows cleaned_data_hotel.latitude cleaned_data_hotel.longitude does not exist, there is no hotel around this location in the database.



3. The recommended_Path.py will create two html files. The first all-amenities file contains all tourist attractions from the hotel to the destination, allowing users to choose freely. The second picture recommends the shortest route through different scenic spots from the starting point to the destination based on the nearest route algorithm, and each scenic spot will only pass once.

   

4. The chain_res_distribution.ipynb will generate the following four html files:

		all_restaurant_plot.html will display the distribution of all restaurants in a dot graph.
		all_restaurant.html will display the distribution of all restaurants in the form of a heat map.
		chain_restaurant_plot.html will display the distribution of all chain restaurants in a dot graph.
		chain_restaurant.html will display the distribution of all chain restaurants in the form of a heat map.
=======
# CMPT353FinalProject
- Reference: https://coursys.sfu.ca/2021fa-cmpt-353-d1/pages/ProjectTour
- WhereShouldIHaveGone: Vancouver Edition
- Group Member: ZhuoLiu WangSiWei TeLiangYu
- Language: Python
