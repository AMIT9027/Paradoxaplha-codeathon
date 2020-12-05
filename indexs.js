function updateMap()
{

fetch("/daat.json")
.then(response=>response.json())
.then(rsp=>
{
console.log(rsp.data)
rsp.data.forEach(element => {
    latitude=element.Latitude;
    longitude=element.Longnitude;
    Name=element.CityName;
    Snapchat=element.Snapchat;
    LinkedIn=element.LinkedIn;
    YouTube=element.YouTube;
    Messenger=element.Messenger;
    Twitter=element.Twitter;
    Instagram=element.Instagram;
    Pinterest=element.Pinterest;
    WhatsApp=element.WhatsApp;
    WeChat=element.WeChat;
    Tumblr=element.Tumblr;
    Skype=element.Skype;
    Viber=element.Viber;
    Tagged=element.Tagged;
    Reddit=element.Reddit;
    Facebook=element.Facebook;
    Discord=element.Discord;
    Telegram=element.Telegram;
    Skyrock=element.Skyrock;
    Classmates=element.Classmates;
    Vine=element.Vine;
    ReverbNation=element.ReverbNation;
    Snapfish=element.Snapfish;
    TikTok=element.TikTok;
    Medium=element.Medium;
    Tagged1=element.Tagged1;
    Renren=element.Renren;
    Badoo=element.Badoo;
    Myspace=element.Myspace;
    StumbleUpon=element.StumbleUpon;
    TheDots=element.TheDots;
    Kiwibox=element.Kiwibox;
    Delicious=element.Delicious;
    Flixster=element.Flixster;
    Ravelry=element.Ravelry;
    Wayn=element.Wayn;
    
    

    color="rgb(255,0,0)"  

new mapboxgl.Marker({

     draggable:false,
     color:color
})
.setLngLat([longitude,latitude])
.setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
.setHTML('<h3>' +Name  + '</h3><p>Snapchat='+Snapchat + '</p><p>LinkedIn=' + LinkedIn+ '</p><p>Twitter='+Twitter + '</p><p>YouTube='+YouTube + '</p><p>Messenger='+Messenger + 
'</p> <p>Instagram='+Instagram + '</p><p>Pinterest='+Pinterest + '</p><p>WhatsApp='+WhatsApp + '</p><p>WeChat='+WeChat + '</p><p>Tumblr='+Tumblr + '</p><p>Skype='+Skype + '</p><p>Viber='+Viber + '</p><p>Tagged='+Tagged + '</p><p>Reddit='+Reddit + 
'</p><p>Facebook='+Facebook + '</p><p>Discord='+Discord + '</p><p>Telegram='+Telegram + '</p><p>Skyrock='+Skyrock + '</p><p>Classmates='+Classmates + '</p><p>Vine='+Vine + '</p><p>ReverbNation='+ReverbNation + '</p><p>Snapfish='+Snapfish + '</p><p>Tik-Tok='+TikTok + '</p><p>Medium='+Medium + 
'</p><p>Tagged1='+Tagged1 +'</p><p>Renren='+Renren +'</p><p>Badoo='+Badoo + '</p><p>Myspace='+Myspace +'</p><p>StumbleUpon='+StumbleUpon + '</p><p>TheDots='+TheDots + '</p><p>Kiwibox='+Kiwibox + '</p><p>Delicious='+Delicious + '</p><p>Flixster='+Flixster + '</p><p>Ravelry='+Ravelry + '</p><p>Wayn='+Wayn + '</p><div><input type="submit" value="NEXT" onclick="Amit()"></input></div>'))
.addTo(map);
});
map.addControl(
    new mapboxgl.GeolocateControl({
    positionOptions: {
    enableHighAccuracy: true
    },
    trackUserLocation: true
    })
    );
})

}

updateMap();
