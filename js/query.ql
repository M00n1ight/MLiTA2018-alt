[out:json][timeout:200]; 
area[name="New York City"]->.b;
( 
way 
(area.b) 
["highway"
 /*~"^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|unclassified_link|residential|residential_link|service|service_link|living_street|pedestrian|road|track)$"*/] 
/*["name"]*/;
node(w); 

); 


out skel;