dataset_ids = {
    'malign': [ 
        # Viral RBDs & Glycoproteins (SARS-1/2, MERS, Flu, HIV, Ebola, Nipah, RSV)
        # Exactly 50 targets. Rigid, pathogenic binding interfaces.
        '6M0J', '7BZ5', '6VW1', '6LZG', '7RBY', '7KLW', '7KMB', '7LM9', '7KGK', '5X4S',
        '6W41', '8K3K', '7D2Z', '7JYC', '7KFV',
        '7LXX', '7JVB', '8ZER', '2GHV', '8YDV',
        '7T9L', '7VNB', '7W9I', '7XBY', '7EAM',
   
    # Influenza Hemagglutinin (Usually crystallized as Chain A)
        '1RVZ', '4O5N', '2VSM', '4L72', '6HJN',
        '1RU7', '1RD8', '5UG0', '2FK0', '4QY1',
        '4O5I', '4JUG', '4JUL', '4ZMJ', '3AL4',
    
    # Nipah, Hendra, RSV, and emerging viruses
        '5JQ3', '8JR5', '4JHW', '5W23', '6TYS',
        '4KR0', '4KQZ', '4N5B', '5X4R', '3BGF'
    ],
    'benign_1_antibodies': [ 
        # Human/Llama Antibodies & Nanobodies (17 targets)
        '1IGT', '1IGY', '5M2J', '6AL5', '7LFB', '7FAB', '4W70', '4TYU', '6APO', '4LAS',
        '1I3V', '1OP9', '4LAR', '1BZQ', '1NQB', '1YQV', '2IG2'
    ],
    'benign_2_receptors': [ 
        # Human Surface Receptors (17 targets)
        '1TIM', '2LYZ', '1AKE', '3PGK', '1MBO', '1FKB', '1G8Q', '4F80',
        '3RRQ', '6OIL', '4F8T', '4J6K', '2PTN', '1RNH', '2X29', '1XED', '4F8Q'
    ],
    'benign_3_synthetic': [ 
        # Safe AI-Designed Binders (16 targets)
        '7S5B', '8U5L', '5TRV', '9XZT', '6W40', '8JPA', '6WI5', '9RGX', '8KDQ', '8HDU',
        '8W97', '8K8G', '8KA7', '5CW9', '8K84', '5CWG'
    ]


}
