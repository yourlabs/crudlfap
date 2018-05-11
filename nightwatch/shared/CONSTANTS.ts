export const CONSTANTS = {
    BASE_URL: 'http://localhost:8000',
    GROUP: {
        BASE_URL: 'http://localhost:8000/group',
        CREATE: 'http://localhost:8000/group/create',
        INPUT: 'Test Group for sample',
        INPUT2: 'Test Group for sample with permission',
        EDIT_INPUT: 'Updated Group',
    },
    ARTIST: {
        BASE_URL: 'http://localhost:8000/artist',
        CREATE: 'http://localhost:8000/artist/create',
        INPUT: 'Test artist for sample',
        INPUT2: 'Test artist for sample with permission',
        EDIT_INPUT: 'Updated artist',
    },
    WAIT_FOR_ELEMENT_VISIBLE_TIMEOUT: 3000,
    PAUSE_TIMEOUT: 3000,
    USER_CREDENTIALS: {
        RIGHT: {
            USERNAME: 'dev',
            PASSWORD: 'dev'
        },
        WRONG: {
            USERNAME: 'dev1',
            PASSWORD: 'dev1'
        }
    },
}