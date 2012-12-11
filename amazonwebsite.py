
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import re
import math
import webbrowser
import ast

#Rules:
#1. Skip items with thumbnail options
#2. Skips pulldown items without prime logo
#3. Price ranges are okay for pulldown w/ prime logo




def main():

    amazonWebsite = AmazonWebsite()

    while True:

        link = str(raw_input("Please enter Amazon.com link: "))
        html = urlopen(link).read()
        Soup = BeautifulSoup(html)

        #print "Marketplace Stock Check: ", amazonWebsite.MarketPlaceStockCheck(Soup)
        #print amazonWebsite.GlobalDescription(Soup, amazonWebsite)
        #print "Amazon Title: ", amazonWebsite.GetTitle(Soup)
        #print "Amazon Price: ", amazonWebsite.GetPrice(Soup)
        #print "Seller Type: ", amazonWebsite.GetSeller(Soup)
        #print "Market Price: ", amazonWebsite.GetMarketPrice(Soup)
        #print "Global Stock Check: ", amazonWebsite.GlobalStockCheck(Soup, amazonWebsite)# Return "In Stock" or "Out of Stock"
        #print "Stock Check: ", amazonWebsite.StockStatus(Soup)
        #print "Global Price Check: ", amazonWebsite.GlobalPriceCheck(Soup, amazonWebsite)
        #print "Global Option: ", amazonWebsite.OptionGlobal(Soup)
        #print amazonWebsite.GetSeller(Soup)
        print amazonWebsite.GetImage(Soup)
        
class AmazonWebsite:
        
    def GlobalStockCheck(self, Soup, amazonWebsite):
        stock_status = "In Stock"
        option_global = amazonWebsite.OptionGlobal(Soup)
        if option_global:
            current_unavail_re = re.compile('<span class="availRed">Currently unavailable.</span><br />') 
            current_unavail_pat = re.findall(current_unavail_re, str(Soup))

            no_stock_re = re.compile('<span class="availRed">Temporarily out of stock.</span>')
            no_stock_pat = re.findall(no_stock_re, str(Soup))

            late_shipment = Soup.find('span', {'class': 'availOrange'})
            late_shipment_re = re.compile('Usually ships within \d+ to \d+ weeks')
            late_shipment_pat = re.findall(late_shipment_re, str(late_shipment))

            late_shipment_re1 = re.compile('Usually ships within \d+ to \d+ days')
            late_shipment_pat1 = re.findall(late_shipment_re1, str(late_shipment))

            notified_avail = Soup.find('span', {'class': 'availRed'})
            notified_avail_re = re.compile('Sign up to be notified when this item becomes available')
            notified_avail_pat = re.findall(notified_avail_re, str(notified_avail))

            if current_unavail_pat:
                stock_status = "Out of Stock"
            if no_stock_pat:
                stock_status = "Out of Stock"
            if late_shipment_pat:
                stock_status = "Out of Stock"
            if late_shipment_pat1:
                stock_status = "Out of Stock"
            if notified_avail_pat:
                stock_status = "Out of Stock"
        else:
            stock_status = amazonWebsite.StockStatus(Soup)
        return stock_status
            
    def StockStatus(self, Soup):
        shipAmazon = re.compile('Ships from and sold by <b>Amazon.com</b>') 
        fulfillAmazon = re.compile('id="SSOFpopoverLink"><strong>Fulfilled by Amazon</strong></a>')
        shipAmazon_flag = re.findall(shipAmazon, str(Soup))
        fulfillAmazon_flag = re.findall(fulfillAmazon, str(Soup))

        current_unavail_re = re.compile('<span class="availRed">Currently unavailable.</span><br />') 
        current_unavail_pat = re.findall(current_unavail_re, str(Soup))
        #print current_unavail_pat

        no_stock_re = re.compile('<span class="availRed">Temporarily out of stock.</span>')
        no_stock_pat = re.findall(no_stock_re, str(Soup))
        #print no_stock_pat

        late_shipment = Soup.find('span', {'class': 'availOrange'})
        late_shipment_re = re.compile('Usually ships within \d+ to \d+ weeks')
        late_shipment_pat = re.findall(late_shipment_re, str(late_shipment))
        #print late_shipment_pat

        late_shipment_re1 = re.compile('Usually ships within \d+ to \d+ days')
        late_shipment_pat1 = re.findall(late_shipment_re1, str(late_shipment))
        #print late_shipment_pat1

        notified_avail = Soup.find('span', {'class': 'availRed'})
        notified_avail_re = re.compile('Sign up to be notified when this item becomes available')
        notified_avail_pat = re.findall(notified_avail_re, str(notified_avail))
        #print notified_avail_pat
        
        stockStatus = 'In Stock'
        if (not shipAmazon_flag and not fulfillAmazon_flag):
            stockStatus = 'Out of Stock'
        if current_unavail_pat:
            stockStatus = 'Out of Stock'
        if no_stock_pat:
            stockStatus = 'Out of Stock'
        if late_shipment_pat:
            stockStatus = 'Out of Stock'
        if notified_avail_pat:
            stockStatus = 'Out of Stock'
        if late_shipment_pat1:
            stockStatus = 'Out of Stock'
        return stockStatus

    def MarketPlaceStockCheck(self, Soup):
        stock_status = "In Stock"
        current_unavail_re = re.compile('<span class="availRed">Currently unavailable.</span><br />') 
        current_unavail_pat = re.findall(current_unavail_re, str(Soup))

        no_stock_re = re.compile('<span class="availRed">Temporarily out of stock.</span>')
        no_stock_pat = re.findall(no_stock_re, str(Soup))

        late_shipment = Soup.find('span', {'class': 'availOrange'})
        late_shipment_re = re.compile('Usually ships within \d+ to \d+ weeks')
        late_shipment_pat = re.findall(late_shipment_re, str(late_shipment))

        notified_avail = Soup.find('span', {'class': 'availRed'})
        notified_avail_re = re.compile('Sign up to be notified when this item becomes available')
        notified_avail_pat = re.findall(notified_avail_re, str(notified_avail))

        late_shipment_re1 = re.compile('Usually ships within \d+ to \d+ days')
        late_shipment_pat1 = re.findall(late_shipment_re1, str(late_shipment))

        if current_unavail_pat:
            stock_status = 'Out of Stock'
        if no_stock_pat:
            stock_status = 'Out of Stock'
        if late_shipment_pat:
            stock_status = 'Out of Stock'
        if notified_avail_pat:
            stock_status = 'Out of Stock'
        if late_shipment_pat1:
            stock_status = 'Out of Stock'
        return stock_status

    def GlobalPriceCheck(self, Soup, amazonWebsite):
        seller_type = amazonWebsite.GetSeller(Soup)
        option_global = amazonWebsite.OptionGlobal(Soup)
        if option_global:
            final_price = amazonWebsite.GetPrice(Soup)
        else:
            if seller_type == 'Sold by Amazon.com':
                final_price = amazonWebsite.GetPrice(Soup)
            elif seller_type == 'Fulfilled by Amazon.com':
                final_price = amazonWebsite.GetPrice(Soup)
            elif seller_type == 'Amazon.com Marketplace Seller':
                final_price = amazonWebsite.GetMarketPrice(Soup)
        return final_price
             

    def GlobalDescription(self, Soup, amazonWebsite):
        description = amazonWebsite.GetDescription(Soup)
        bullet = amazonWebsite.GetBullets(Soup)
        bullet_variation = amazonWebsite.GetBulletsVariation(Soup)
        option = amazonWebsite.OptionGlobal(Soup)
        if not option:
            final_description = """
                            %s
                            <br>
                            %s""" % (description, bullet)
        elif option:
            final_description = """
                            %s
                            <br>
                            %s
                            <br>
                            %s""" % (description, bullet, bullet_variation)

        return final_description
            
                  
    def GetPrice(self, Soup):
        price = Soup.find('td', {'id': 'actualPriceContent'})
        price1 = Soup.find('span', {'class': 'priceLarge'})
        price2 = Soup.find('div', {'class': 'pricetext'})
        if price:
            price_re = re.compile('<b class="priceLarge">(\$.*?)</b>')
            price_pat = re.findall(price_re, str(price))
            finalPrice = str(price_pat[0])
            finalPrice = finalPrice[1:]
        elif price1:
            price_re = re.compile('\$(\d+\.\d+)')
            price_pat = re.findall(price_re, str(price1))
            for i in price_pat:
                finalPrice = i
        elif price2:
            price_re = re.compile('\$(\d+\.\d+)')
            price_pat = re.findall(price_re, str(price2))
            for i in price_pat:
                finalPrice = i
        else:
            pass     
        return finalPrice

    def GetMarketPrice(self, Soup):
        marketPrice = Soup.find('td', {'id': 'actualPriceContent'})
        marketShipping = Soup.find('div', {'id': 'BBPricePlusShipID'})
        if marketPrice:
            marketPrice_re = re.compile('<b class="priceLarge">\$(.*)</b></span>')
            marketPrice_pat = re.findall(marketPrice_re, str(marketPrice))
            for i in marketPrice_pat:
                marketPrice_final = i
        if marketShipping:
            marketShipping_re = re.compile('<span class="plusShippingText">.*\$(.*).*shipping</span>')
            marketShipping_pat = re.findall(marketShipping_re, str(marketShipping))
            for i in marketShipping_pat:
                i = i.replace('&nbsp;', '')
                marketShipping_final = i
        if marketPrice and marketShipping:
            try:
                finalPrice = float(marketPrice_final) + float(marketShipping_final) #Takes care of if shipping if free
            except:
                finalPrice = float(marketPrice_final)
        else:
            finalPrice = ''
        return finalPrice
        
    def GetSeller(self, Soup):
        amazon = str(Soup.find('div', {'style': 'padding-bottom: 0.75em;'}))
        amazonIndex = amazon.find('<script type="text/javascript">')
        amazon = amazon[:amazonIndex].strip()
        amazonSeller = 'Ships from and sold by <b>Amazon.com</b>'
        amazonFulfilled = 'id="SSOFpopoverLink"><strong>Fulfilled by Amazon</strong></a>'
        finalSeller = ''
        if amazonSeller in amazon:
            statusSeller = 'Sold by Amazon.com'
        elif amazonFulfilled in amazon:
            amazonFulfilled_re = re.compile('</span><br /> Sold by <b><a href=".*">(.*)</a></b>')
            amazonFulfilled_pat = re.findall(amazonFulfilled_re, amazon)
            for i in amazonFulfilled_pat:
                finalSeller = i
            statusSeller = 'Fulfilled by Amazon.com'
        else:
            marketSeller_re = re.compile('</span><br /> Ships from and sold by <b><a href=".*">(.*)</a></b>')
            marketSeller_pat = re.findall(marketSeller_re, amazon)
            for i in marketSeller_pat:
                    finalSeller = i
            statusSeller = 'Amazon.com Marketplace Seller' 
        return statusSeller

    
    def GetTitle(self, Soup):
        book_dvd_title = Soup.find('h1', {'class': 'parseasinTitle '})
        amazon_variation_title = Soup.find('span', {'id': 'btAsinTitle'})
        if amazon_variation_title: 
            regex = re.compile('>(.*)<')
            regex_pat = re.findall(regex, str(amazon_variation_title))
            for i in regex_pat:
                finalTitle = i
                finalTitle = finalTitle.replace('<span style="text-transform: capitalize; font-size: 16px;">', '')
                finalTitle = finalTitle.replace('</span>', '')
                finalTitle = finalTitle.strip()
        elif book_dvd_title:
            regex = re.compile('<span id="btAsinTitle">(.*?) <')
            regex_pat = re.findall(regex, str(book_dvd_title))
            for i in regex_pat:
                finalTitle = str(i)
                finalTitle = finalTitle.replace('<span style="text-transform: capitalize; font-size: 16px;">', '')
                finalTitle = finalTitle.replace('</span>', '')
        else:
            finalTitle = ''
        return finalTitle
                

    def GetImage(self, Soup):
        #print Soup
        image_list = []
        image = Soup.find('div', {'id': 'rwImages_hidden'})
        image1 = Soup.find('div', {'id': 'prodImageOuter'})
        image2 = Soup.find('div', {'class': 'new-faceout'})
        amazon_marketplaceseller_image = Soup.find('td', {'id': 'prodImageCell'})
        amazon_prime_image = Soup.find('div', {'id': 'prodImageCell'})
        option_variation_image = Soup.find('table', {'class': 'bxgy-bundle'}) 
        image_re = re.compile('imageObj.src = "(.*?)";')
        image_pat = re.findall(image_re, str(Soup))
        image1 = Soup.find('tr', {'id': 'prodImageContainer'})
        if option_variation_image:
            image_re = re.compile('src="(.*?)"')
            image_pat_variation = re.findall(image_re, str(option_variation_image))
            final_image_list = image_pat_variation
        elif image_pat:
            final_image_list = image_pat
        elif image1:
            image1_re = re.compile('src="(.*?)"')
            image1_pat = re.findall(image1_re, str(image1))
            final_image_list = image1_pat
        elif image2:
            image2_re = re.compile('src="(.*?)"')
            image2_pat = re.findall(image2_re, str(image2))
            final_image_list = image2_pat
        if len(final_image_list) > 1:
            image_list.append(str(final_image_list[0]))
            return image_list
        else:
            return final_image_list
                          
    def GetDescription(self, Soup):
        description = Soup.findAll('div', {'class': 'productDescriptionWrapper'})
        if description:
            if len(description) != 1:
                description = str(description[1])         
                index = description.find('<div class="emptyClear">')
                finalDescription = description[:index].strip()
            else:
                description = str(description[0])
                index = description.find('<div class="emptyClear">')
                finalDescription = description[:index].strip()
        else:
            finalDescription = ''
        if finalDescription:
            try:
                flag = "Eligible for Free Returns on qualified Clothing, Shoes, Jewelry, Watches, Luggage, Accessories, and Sunglasses fulfilled by Amazon."
                if flag in finalDescription:
                    index = finalDescription.find(flag)
                    finalDecription = finalDescription[:index].split()

                flag2 = '<img src="http://g-ecx.images-amazon.com.*</center>'
                if flag2 in finalDescription:
                    index = finalDescription.find(flag2)
                    index += 100
                    finalDescription = finalDescription[index:]
                flag3 = '</center>'
                if flag3 in finalDescription:
                    index = finalDescription.find(flag3)
                    finalDescription = finalDescription[index:]
            except:
                pass
        return finalDescription

    def GetBullets(self, Soup):
        finalBullets = ''
        bullets = Soup.find('ul', {'style': 'list-style-type: disc; margin-left: 25px;'})
        if bullets:
            finalBullets = bullets
        else:
            bullets = Soup.find('ul', {'style': 'list-style: disc; padding-left: 25px;'})
            if bullets:
                finalBullets = bullets
            else:
                bullets = Soup.find('div', {'id': 'feature-bullets_feature_div'})
                if bullets:
                    finalBullets = bullets
                else:
                    finalBullets = ''          
        return finalBullets


    def OptionGlobal(self, Soup):
        #Ensures amazon.com listing has pulldown menu and meniton selecting an option in add to cart table
        pulldown_prompt = Soup.find('div', {'id': 'dropdown_size_name'}) #Please select an options message in add to cart box
        pulldown_message = Soup.find('div', {'id': 'twisterAddToCartOrig'}) #clothing
        pulldown_message1 = Soup.find('select', {'name': 'asin-redirect'}) #rings
        thumbnail_option_color = Soup.findAll('div', {'key': 'color_name'}) #Thumbnail Color Options
        thumbnail_option_size = Soup.findAll('div', {'key': 'size_name'})
        if thumbnail_option_color or thumbnail_option_size:
            option_status = "Thumbnail Options"
            final_option_list = []
        else:
            if pulldown_prompt and pulldown_message:
                pulldown = str(Soup.find('div', {'id': 'dropdown_size_name'}))
                pulldown_re = re.compile('<option value="\d+" title=".*?" style="color:#\d+;">(.*?)</option>')
                pulldown_pat = re.findall(pulldown_re, pulldown)
                final_option_list = pulldown_pat
                option_status = "Pulldown Options"
            elif pulldown_message1:
                pulldown = str(Soup.find('select', {'name': 'asin-redirect'}))
                pulldown_re = re.compile('<option value=".*?" title=".*?">(.*?)</option>')
                pulldown_pat = re.findall(pulldown_re, pulldown)
                final_option_list = pulldown_pat
                option_status = "Pulldown Options"
            else:
                final_option_list = []
                option_status = "No Options"
        return final_option_list
            
            
    def PullDownOption(self, Soup):
        pulldown1 = Soup.find('div', {'id': 'dropdown_size_name'})
        if pulldown1:
            pulldown1 = str(pulldown1)
            pulldown1_re = re.compile('<option value="\d+" title=".*?" style="color:#\d+;">(.*?)</option>')
            pulldown1_pat = re.findall(pulldown1_re, pulldown1)
            final_option_list = pulldown1_pat
        else:
            final_option_list = []
        return final_option_list

    def ThumbNailOption(self, Soup):
        final_option_list = []
        thumbnail = Soup.findAll('div', {'key': 'color_name'})
        if thumbnail:
            for i in thumbnail:
                thumb_nail_re = re.compile('relative">(.*?)</div>')
                thumb_nail_pat = re.findall(thumb_nail_re, str(i))
                for i in thumb_nail_pat:
                    final_option_list.append(i)
        return final_option_list

    def GetBulletsVariation(self, Soup):
        bullet_string = ''
        bullet_variation = Soup.find('div', {'id': 'feature-bullets-atf'})
        if bullet_variation:
            bullet_variation = str(bullet_variation)
            bullet_variation_re = re.compile('<li><span>(.*?)</span></li>')
            bullet_variation_pat = re.findall(bullet_variation_re, bullet_variation)
            for i in bullet_variation_pat:
                bullet_string += i + "\n"
        else:
            bullet_string = ''
        return bullet_string

    def GetTechDetails(self, Soup):
        tech_details_string = ''
        tech_details = Soup.find('div', {'class': 'bucket'})
        if tech_details:
            index = str(tech_details).find('<div id="technicalProductFeatures"></div>')
            tech_details_re = re.compile('<li>(.*?)</li>')
            tech_details_pat = re.findall(tech_details_re, str(tech_details)[:index])
            for i in tech_details_pat:
                tech_details_string += i + "\n"       
        return tech_details_string

    def OrangeDetail(self, Soup):
        orange_details = Soup.find('span', {'class': 'availOrange'})
        if orange_details:
            final_orange_details = str(orange_details)
        else:
            final_orange_details = ''
        return final_orange_details

    #def PullDownPrice(self, Soup):
    #    pulldown_price = str(Soup.find('span', {'class': 'priceLarge'}))
    #    pulldown_price_re = re.compile
        
                    
if __name__ == "__main__":
    main()
