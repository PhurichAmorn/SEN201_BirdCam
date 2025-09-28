set total_items = 0
set total_vat = 0
set grand_total = 0
for item in item_set
    set vat = 0
    if item_price >= 100
        Set vat = item_price * 0.07
    endif
    print "Name: {item_name} Price: {item_price} VAT: {vat} Price+VAT: {item_price + vat}"
    set total_items = total_items + item_price
    set total_vat = total_vat + vat
    set grand_total = grand_total + item_price + vat
endfor
print "Number of item: {total_items}, VAT: {total_vat}฿, Total: {grand_total}฿"