LEVELS = [
    # Level 1: Full rows with gaps
    [
        [1]*20,
        [1 if i % 2 == 0 else 0 for i in range(20)],
        [1]*20,
        [1]*20,
        [1 if i % 3 == 0 else 0 for i in range(20)],
    ],

    # Level 2: Border + indestructible center
    [
        [1]*20,
        [1] + [0]*18 + [1],
        [1] + [0]*9 + [2] + [0]*9 + [1],
        [1] + [0]*18 + [1],
        [1]*20,
        [1]*10 + [2] + [1]*9,
    ],

    # Level 3: Pyramid with indestructible shell
    [
        [0]*8 + [1]*4 + [0]*8,
        [0]*7 + [2]*6 + [0]*7,
        [0]*6 + [1]*8 + [0]*6,
        [0]*5 + [1,2]*5 + [0]*5,
        [0]*4 + [1]*12 + [0]*4,
        [0]*4 + [2]*12 + [0]*4,
    ],

    # Level 4: Checkerboard with indestructibles
    [
        [2 if (i + j) % 6 == 0 else 1 if (i + j) % 2 == 0 else 0 for i in range(20)] for j in range(7)
    ],

    # Level 5: Hourglass + thick outer shell
    [
        [2]*20,
        [0,1]*9 + [0,1],
        [2 if i % 3 == 0 else 1 for i in range(20)],
        [0,0,1]*6 + [0,0],
        [0,0,1]*6 + [0,0],
        [2 if i % 4 == 1 else 1 for i in range(20)],
        [0,1]*9 + [0,1],
        [2]*10,
    ],

    # Level 6: Zigzag with embedded indestructibles
    [
        [2 if (i + j) % 5 == 0 else 1 if (i + j) % 3 == 0 else 0 for i in range(20)] for j in range(8)
    ],

    # Level 7: Diamond with indestructible core
    [
        [0]*9 + [1] + [0]*10,
        [0]*8 + [1,1,1] + [0]*8,
        [0]*7 + [1,2,1,2,1] + [0]*7,
        [0]*6 + [1,1,1,1,1,1,1] + [0]*6,
        [0]*5 + [1]*9 + [0]*6,
        [0]*6 + [2]*7 + [0]*7,
        [0]*7 + [1]*5 + [0]*8,
        [0]*8 + [2,1,2] + [0]*8,
        [0]*9 + [1] + [0]*10,
    ],

    # Level 8: Spiral illusion with inner core
    [
        [2]*20,
        [2]+[0]*18+[2],
        [2]+[0]+[1]*16+[0]+[2],
        [2]+[0]*2+[1]*14+[0]*2+[2],
        [2]+[0]*3+[2]*12+[0]*3+[2],
        [2]+[0]*4+[1]*10+[0]*4+[2],
        [2]*10,
    ],

    # Level 9: Arrows with heavy indestructibles
    [
        [0,0,1,0,0]*4,
        [2,1,2,1,2]*4,
        [1]*20,
        [2 if i % 2 == 0 else 1 for i in range(20)],
        [1]*20,
        [0,1]*10,
    ],

    # Level 10: Two Towers reinforced
    [
        [1]*4 + [0]*12 + [1]*4,
        [1]*4 + [0]*12 + [1]*4,
        [2]*4 + [0]*12 + [2]*4,
        [1]*4 + [0]*12 + [1]*4,
        [2]*4 + [0]*12 + [2]*4,
        [1]*4 + [0]*12 + [1]*4,
        [1]*20,
        [2 if i % 3 == 0 else 1 for i in range(20)],
    ]
]
